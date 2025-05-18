from pygame import Rect
from libc.stdlib cimport malloc, free
from libc.math cimport fabsf, fminf
from libc.stdint cimport int16_t, uint16_t


cdef struct MouseField:
    int16_t X
    int16_t Y
    int16_t W
    int16_t H



cdef class Component:

    cdef public float X
    cdef public float Y
    cdef public float _X
    cdef public float _Y

    cdef public int16_t W
    cdef public int16_t H

    cdef MouseField *MouseFields
    cdef uint16_t MouseFields_Size


    def __cinit__(self):
        self.MouseFields = NULL
        self.MouseFields_Size = 0


    def __dealloc__(self):
        free(self.MouseFields)


    def __init__(self, int16_t x, int16_t y, int16_t w, int16_t h):
        self.X = x
        self._X = x
        self.Y = y
        self._Y = y
        self.W = w
        self.H = h


    cpdef void newMouseFields(self, uint16_t size):
        if self.MouseFields != NULL:
            free(self.MouseFields)

        self.MouseFields = <MouseField*> malloc(sizeof(MouseField) * size)
        self.MouseFields_Size = size


    cpdef void setMouseField(self, uint16_t Index, int16_t X, int16_t Y, int16_t W, int16_t H):
        if self.MouseFields_Size > Index:
            self.MouseFields[Index].X = X
            self.MouseFields[Index].Y = Y
            self.MouseFields[Index].W = W
            self.MouseFields[Index].H = H

    
    cpdef void setMouseField_DisplayPos(self, uint16_t index, int16_t X, int16_t Y, int16_t W, int16_t H):
        self.setMouseField(index, X - <int16_t>self.X, Y - <int16_t>self.Y, W, H)


    cpdef bint collidepoint(self, uint16_t index, tuple point):

        if index >= self.MouseFields_Size or index < 0:
            return False

        cdef int16_t x = <int16_t> point[0]
        cdef int16_t y = <int16_t> point[1]

        cdef int16_t cX = <int16_t> self.X + self.MouseFields[index].X
        cdef int16_t cY = <int16_t> self.Y + self.MouseFields[index].Y

        return x > cX and y > cY and x < cX + self.MouseFields[index].W and y < cY + self.MouseFields[index].H



    cpdef void MoveTo(self, float X, float Y):
        self.X = X
        self._X = X
        self.Y = Y
        self._Y = Y


    cpdef void Animate_X(self, float Target, float Speed, float AO):
        if fabsf(self.X - Target) < 1:
            self.X = Target
        else:
            self.X += (Target - self.X) * AO * Speed

    
    cpdef void Animate_Y(self, float Target, float Speed, float AO):
        if fabsf(self.Y - Target) < 1:
            self.Y = Target
        else:
            self.Y += (Target - self.Y) * AO * Speed

    
    cpdef void AnimateSpdUp_X(self, bint Negative, float Start, float Target, float Speed, float AO):
        if Negative: # -
            if self.X > Target:
                self.X -= ((fabsf(self.X - Start) + 1) * AO * Speed)
            else:
                self.X = Target
        else: # +
            if self.X < Target:
                self.X += ((fabsf(self.X - Start) + 1) * AO * Speed)
            else:
                self.X = Target

        
    cpdef void AnimateSpdUp_Y(self, bint Negative, float Start, float Target, float Speed, float AO):
        if Negative: # -
            if self.Y > Target:
                self.Y -= ((fabsf(self.Y - Start) + 1) * AO * Speed)
            else:
                self.Y = Target
        else: # +
            if self.Y < Target:
                self.Y += ((fabsf(self.Y - Start) + 1) * AO * Speed)
            else:
                self.Y = Target

    

    cpdef object calculateRect(self):
        cdef float _x = self._X
        cdef float _y = self._Y
        cdef float dx = fabsf(self.X - _x)
        cdef float dy = fabsf(self.Y - _y)

        if dy or dx:
            self._X = self.X
            self._Y = self.Y

            return Rect(fminf(self.X, _x) - 1, fminf(self.Y, _y) - 1, self.W + dx + 2, self.H + dy + 2)
        else:
            return Rect(self.X, self.Y, self.W, self.H)


    
    cpdef object calculateTrailRect_X(self):
        cdef float dx = self.X - self._X

        if dx >= 0:
            return Rect(<int>self._X - 1, <int>self.Y, <int>fabsf(dx) + 1, self.H)
        else:
            return Rect(<int>self.X + self.W + 1, <int>self.Y, <int>fabsf(dx) + 1, self.H)


    cpdef object calculateTrailRect_Y(self):
        cdef float dy = self.Y - self._Y

        if dy >= 0:
            return Rect(<int>self.X, <int>self._Y - 1, self.W, <int>fabsf(dy) + 1)
        else:
            return Rect(<int>self.X, <int>self.Y + self.H, self.W, <int>fabsf(dy) + 1)
    


    def Reset(self, int x, int y): ...
    def Update(self, float A_OFFSET): ...
    def Frame(self, object DISP): ...
    
    def MouseMotion(self, tuple POS): ...
    def MouseButtonDown(self, tuple POS, int BUTTON): ...
    def MouseButtonUp(self, tuple POS, int BUTTON): ...
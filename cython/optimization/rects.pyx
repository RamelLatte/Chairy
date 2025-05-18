from libc.stdint cimport int16_t, uint16_t
from libc.stdlib cimport malloc, free



cdef struct Geometry:

    int16_t X
    int16_t Y
    int16_t W
    int16_t H


cdef class RectList:

    cdef Geometry *Arr
    cdef readonly uint16_t Size

    cdef uint16_t Index


    def __init__(self, uint16_t size):

        self.Arr = <Geometry*> malloc(sizeof(Geometry) * size)
        self.Size = size

        self.Index = 0


    def __dealloc__(self):
        free(self.Arr)


    cpdef void append(self, int16_t X, int16_t Y, int16_t W, int16_t H):
        self.Arr[self.Index].X = X
        self.Arr[self.Index].Y = Y
        self.Arr[self.Index].W = W
        self.Arr[self.Index].H = H
        self.Index += 1


    cpdef int collide_index(self, int16_t X, int16_t Y, int16_t W, int16_t H):
        cdef Geometry* g
        cdef int gx, gy, gw, gh

        for i in range(self.Index):  # Index까지만 검사 (현재 유효한 데이터)
            g = self.Arr + i

            gx = g.X
            gy = g.Y
            gw = g.W
            gh = g.H

            if not (X + W <= gx or X >= gx + gw or Y + H <= gy or Y >= gy + gh):
                return i  # 충돌하는 인덱스 반환

        return -1  # 충돌 없음


    cpdef tuple getCoordinate(self, uint16_t Index):
        return (self.Arr[Index].X, self.Arr[Index].Y)
from libc.stdint cimport int16_t, uint16_t
from libc.stdlib cimport malloc, free, realloc
from libc.string cimport memcpy
from pygame import Rect


cdef struct Geometry:

    int16_t X
    int16_t Y
    int16_t W
    int16_t H



### Optimized Rect List ###


cdef class RectList:

    cdef Geometry *Arr
    cdef readonly uint16_t Size

    cdef readonly uint16_t Length


    def __cinit__(self, uint16_t size):

        self.Arr = <Geometry*> malloc(sizeof(Geometry) * size)
        self.Size = size

        self.Length = 0


    def __dealloc__(self):
        free(self.Arr)


    cpdef void append(self, int16_t X, int16_t Y, int16_t W, int16_t H):
        self.Arr[self.Length].X = X
        self.Arr[self.Length].Y = Y
        self.Arr[self.Length].W = W
        self.Arr[self.Length].H = H
        self.Length += 1


    cpdef object get(self, uint16_t Index):
        return Rect(self.Arr[Index].X, self.Arr[Index].Y, self.Arr[Index].W, self.Arr[Index].H)

    
    cpdef void clear(self):
        self.Length = 0


    cpdef int colliderect(self, int16_t X, int16_t Y, int16_t W, int16_t H):
        cdef int gx, gy, gw, gh

        for i in range(self.Length):  # Index까지만 검사 (현재 유효한 데이터)
            gx = self.Arr[i].X
            gy = self.Arr[i].Y
            gw = self.Arr[i].W
            gh = self.Arr[i].H

            if not (X + W <= gx or X >= gx + gw or Y + H <= gy or Y >= gy + gh):
                return i  # 충돌하는 인덱스 반환

        return -1  # 충돌 없음

    
    cpdef int collidepoint(self, int16_t X, int16_t Y):
        cdef int gx, gy, gw, gh

        for i in range(self.Length):  # Index까지만 검사 (현재 유효한 데이터)
            gx = self.Arr[i].X
            gy = self.Arr[i].Y
            gw = self.Arr[i].W
            gh = self.Arr[i].H

            if X >= gx and X <= gx + gw and Y >= gy and Y <= gy + gh:
                return i  # 충돌하는 인덱스 반환

        return -1  # 충돌 없음


    cpdef tuple getCoordinate(self, uint16_t Index):
        return (self.Arr[Index].X, self.Arr[Index].Y)



### Dirty Rectangles ###


cdef class GeometryArray:
    cdef Geometry* arr
    cdef int size
    cdef int length

    def __cinit__(self, int init_size=64):
        self.arr = <Geometry*> malloc(sizeof(Geometry) * init_size)
        self.size = init_size
        self.length = 0

    def __dealloc__(self):
        if self.arr != NULL:
            free(self.arr)

    cdef void append(self, Geometry g):
        if self.length >= self.size:
            self.size *= 2
            self.arr = <Geometry*> realloc(self.arr, sizeof(Geometry) * self.size)
        self.arr[self.length] = g
        self.length += 1

    cdef void delete(self, int index):
        cdef int i
        for i in range(index, self.length - 1):
            self.arr[i] = self.arr[i + 1]
        self.length -= 1

    cdef Geometry get(self, int index):
        return self.arr[index]



# 겹침 여부 함수
cdef bint is_overlap(Geometry a, Geometry b):
    return not (
        a.X + a.W <= b.X or b.X + b.W <= a.X or
        a.Y + a.H <= b.Y or b.Y + b.H <= a.Y
    )


# 사각형 병합 함수
cdef Geometry merge_rects(Geometry a, Geometry b):
    cdef Geometry m
    cdef int x1 = min(a.X, b.X)
    cdef int y1 = min(a.Y, b.Y)
    cdef int x2 = max(a.X + a.W, b.X + b.W)
    cdef int y2 = max(a.Y + a.H, b.Y + b.H)

    m.X = x1
    m.Y = y1
    m.W = x2 - x1
    m.H = y2 - y1
    return m


cdef class DirtyRectsManager:

    cdef Geometry *Arr
    cdef Geometry *Prior

    cdef uint16_t Prior_Length
    cdef uint16_t Length


    def __cinit__(self):

        self.Arr = <Geometry*> malloc(sizeof(Geometry) * 512)
        self.Prior = <Geometry*> malloc(sizeof(Geometry) * 0)

        self.Prior_Length = 0
        self.Length = 0


    def __dealloc__(self):
        free(self.Arr)
        free(self.Prior)


    cpdef void append(self, int16_t X, int16_t Y, int16_t W, int16_t H):
        self.Arr[self.Length].X = X
        self.Arr[self.Length].Y = Y
        self.Arr[self.Length].W = W
        self.Arr[self.Length].H = H
        self.Length += 1


    cpdef list calculate(self):
        cdef GeometryArray merged = GeometryArray(self.Length + self.Prior_Length + 8)
        cdef Geometry current, other
        cdef int i, j
        cdef bint did_merge
        cdef list result = []

        # 병합 배열 초기화
        for i in range(self.Length):
            merged.append(self.Arr[i])
        for i in range(self.Prior_Length):
            merged.append(self.Prior[i])

        # Prior 갱신
        if self.Prior != NULL:
            free(self.Prior)

        self.Prior = <Geometry*> malloc(sizeof(Geometry) * self.Length)
        memcpy(self.Prior, self.Arr, sizeof(Geometry) * self.Length)
        self.Prior_Length = self.Length

        # 병합 루프
        while True:
            did_merge = False
            i = 0
            while i < merged.length:
                current = merged.get(i)
                j = i + 1
                while j < merged.length:
                    other = merged.get(j)
                    if is_overlap(current, other):
                        current = merge_rects(current, other)
                        merged.arr[i] = current
                        merged.delete(j)
                        did_merge = True
                        # j는 그대로 유지 → 새로 당겨온 값도 다시 검사
                    else:
                        j += 1
                i += 1
            if not did_merge:
                break

        # 결과 리스트
        for i in range(merged.length):
            current = merged.get(i)
            result.append(Rect(current.X, current.Y, current.W, current.H))

        # 초기화
        self.Length = 0

        return result
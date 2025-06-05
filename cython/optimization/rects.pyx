from libc.stdint cimport int16_t, uint16_t
from libc.stdlib cimport malloc, free, realloc
from pygame import Rect
from array import array


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

    cdef uint16_t Init_Size
    cdef uint16_t Size
    cdef uint16_t Length

    cdef readonly bint Full


    def __cinit__(self, uint16_t init_size = 48):

        self.Init_Size = init_size

        self.Arr = <Geometry*> malloc(sizeof(Geometry) * self.Init_Size)

        self.Size = 64
        self.Length = 0

        self.Full = False


    def __dealloc__(self):
        if self.Arr != NULL:
            free(self.Arr)


    cdef void _append(self, Geometry g):
        if self.Length >= self.Size:
            self.Size += 32
            self.Arr = <Geometry*> realloc(self.Arr, sizeof(Geometry) * self.Size)
        self.Arr[self.Length] = g
        self.Length += 1


    cdef void _delete(self, int index):
        cdef int i
        for i in range(index, self.Length - 1):
            self.Arr[i] = self.Arr[i + 1]
        self.Length -= 1


    cdef Geometry _get(self, int index):
        return self.Arr[index]


    cpdef void updateFull(self):
        self.Full = True
        self.Arr[0].X = 0
        self.Arr[0].Y = 0
        self.Arr[0].W = 1920
        self.Arr[0].H = 1080
        self.Length = 1


    cpdef void append(self, int[::1] RectValue):
        if self.Full:
            return
        cdef Geometry g
        g.X = RectValue[0]
        g.Y = RectValue[1]
        g.W = RectValue[2]
        g.H = RectValue[3]
        self._append(g)


    cpdef void appendRect(self, object Rect):
        if self.Full:
            return
        cdef Geometry g
        g.X = Rect.left
        g.Y = Rect.top
        g.W = Rect.width
        g.H = Rect.height
        self._append(g)


    cpdef void calculate(self):

        # 화면 전체 업데이트인 경우
        if self.Full:
            return

        # 아닌 경우 Dirty Rectangles 계산
        cdef Geometry current, other
        cdef int i, j
        cdef bint did_merge

        # 병합 루프
        while True:
            did_merge = False
            i = 0
            while i < self.Length:
                current = self._get(i)
                j = i + 1
                while j < self.Length:
                    other = self._get(j)
                    if is_overlap(current, other):
                        current = merge_rects(current, other)
                        self.Arr[i] = current
                        self._delete(j)
                        did_merge = True
                        # j는 그대로 유지 → 새로 당겨온 값도 다시 검사
                    else:
                        j += 1
                i += 1
            if not did_merge:
                break


    cpdef list get(self):

        # 화면 전체 업데이트인 경우
        if self.Full:
            return [Rect(0, 0, 1920, 1080)]

        cdef list result = []
        cdef Geometry current

        for i in range(self.Length):
            current = self._get(i)
            result.append(Rect(current.X, current.Y, current.W, current.H))

        return result

    
    cpdef list clear(self):
        self.Size = self.Init_Size
        self.Arr = <Geometry*> realloc(self.Arr, sizeof(Geometry) * self.Size)
        self.Length = 0


    cpdef bint empty(self):
        return self.Length == 0


    def iter(self) -> array:
        for i in range(self.Length):
            yield array('i', [self.Arr[i].X, self.Arr[i].Y, self.Arr[i].W, self.Arr[i].H])


cdef class EmptyDRManager:


    cpdef void updateFull(self):
        ...


    cpdef void append(self, int[::1] RectValue):
        ...


    cpdef void appendRect(self, object Rect):
        ...


    cpdef list calculate(self):
        ...
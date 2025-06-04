from pygame import Rect
from array import array


class RectList:

    Length: int

    def __init__(self, size: int):
        ...

    def append(self, X: int, Y: int, W: int, H: int):
        ...

    def get(self, Index: int) -> Rect:
        ...

    def clear(self):
        ...

    def colliderect(self, X: int, Y: int, W: int, H: int) -> int:
        """
        **-1이 반환되면 충돌되는 영역이 없다는 뜻임.** 
        **모든 매개변수는 항상 값이 -32767~32767 사이여야 함!**
        """
        ...

    def collidepoint(self, X: int, Y: int) -> int:
        """
        **-1이 반환되면 충돌되는 영역이 없다는 뜻임.** 
        **모든 매개변수는 항상 값이 -32767~32767 사이여야 함!**
        """
        ...

    def getCoordinate(self, Index: int) -> tuple[int]:
        ...


class DirtyRectsManager:

    def __init__(self, init_size: int = 48):
        ...

    def updateFull(self):
        ...

    def append(self, RectValue: array):
        ...

    def appendRect(self, Rect: Rect):
        ...

    def calculate(self) -> list[Rect]:
        ...


class EmptyDRManager:

    def __init__(self, init_size: int = 48):
        ...

    def updateFull(self):
        ...

    def append(self, RectValue: array):
        ...

    def appendRect(self, Rect: Rect):
        ...

    def calculate(self) -> list[Rect]:
        ...
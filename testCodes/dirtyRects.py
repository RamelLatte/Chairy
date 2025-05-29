
from optimization.rects import DirtyRectsManager as OptimizedDirtyRectsManager
from pygame import Rect
from random import randint
from time import time


class DirtyRectsManager:

    def __init__(self):
        self.current = []  # 이번 프레임
        self.prior = []    # 이전 프레임

    def append(self, x: int, y: int, w: int, h: int):
        self.current.append((x, y, w, h))

    def is_overlap(self, a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return not (
            ax + aw <= bx or bx + bw <= ax or
            ay + ah <= by or by + bh <= ay
        )

    def merge_rects(self, a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b

        x1 = min(ax, bx)
        y1 = min(ay, by)
        x2 = max(ax + aw, bx + bw)
        y2 = max(ay + ah, by + bh)

        return (x1, y1, x2 - x1, y2 - y1)

    def calculate(self):
        merged = self.current + self.prior
        result = []

        self.prior = self.current[:]

        while True:
            did_merge = False
            i = 0
            while i < len(merged):
                current = merged[i]
                j = i + 1
                while j < len(merged):
                    if self.is_overlap(current, merged[j]):
                        current = self.merge_rects(current, merged[j])
                        merged[i] = current
                        del merged[j]
                        did_merge = True
                    else:
                        j += 1
                i += 1

            if not did_merge:
                break

        # 결과 리스트 생성
        for rect in merged:
            result.append(Rect(*rect))

        # Prior 백업 및 초기화
        self.current.clear()

        return result


### 테스트 코드 ###

manager = DirtyRectsManager()

start = time()

for i in range(100):
    for j in range(128):
        manager.append(randint(-32767, 32767), randint(-32767, 32767), randint(-32767, 32767), randint(-32767, 32767))

    manager.calculate()

print("Pure Python Dirty Rects:", time() - start, "sec")


o_manager = OptimizedDirtyRectsManager()

start = time()

for i in range(100):
    for j in range(128):
        o_manager.append(randint(-32767, 32767), randint(-32767, 32767), randint(-32767, 32767), randint(-32767, 32767))

    o_manager.calculate()

print("  Optimized Dirty Rects:", time() - start, "sec")

manager = DirtyRectsManager()
o_manager = OptimizedDirtyRectsManager()

fail = False

for i in range(1000):
    for j in range(512):
        a = randint(-1920, 1920)
        b = randint(-1080, 1080)
        c = randint(0, 1920)
        d = randint(0, 1080)

        o_manager.append(a, b, c, d)
        manager.append(a, b, c, d)

    A = len(manager.calculate())
    B = len(o_manager.calculate())

    if A != B:
        print(A, ",", B)
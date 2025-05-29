
from optimization.rects import RectList
from pygame import Rect
from random import randint
from time import time


start = time()

rects: list[Rect] = []

for j in range(100):
    rects.append(Rect(randint(0, 1000), randint(0, 1000), randint(0, 1000), randint(0, 1000)))

for i in range(100000):
    for i, r in enumerate(rects):
        r.collidepoint(randint(-32767, 32767), randint(-32767, 32767))

print("Pure Python Rects:", time() - start, "sec")

start = time()

list = RectList(100)

for j in range(100):
    list.append(randint(0, 1000), randint(0, 1000), randint(0, 1000), randint(0, 1000))

for i in range(100000):
    index = list.collidepoint(randint(-32767, 32767), randint(-32767, 32767))
    if index != -1:
        r = list.get(index)

print("  Optimized Rects:", time() - start, "sec")
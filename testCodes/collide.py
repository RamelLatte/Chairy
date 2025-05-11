
from optimization.positioning import collidepoint
from pygame import Rect
from time import time
from random import randint

start = time()

for j in range(1000):
    pos = (randint(-100, 200), randint(-100, 200))
    for i in range(10000):
        if Rect(100, 100, 100, 100).collidepoint(pos):
            ...
        else:
            ...

print("Pygame Rect:", time() - start, "sec")

start = time()

for j in range(1000):
    pos = (randint(-100, 200), randint(-100, 200))
    for i in range(10000):
        if collidepoint(100, 100, 100, 100, pos):
            ...
        else:
            ...

print("Optimized Rect:", time() - start, "sec")
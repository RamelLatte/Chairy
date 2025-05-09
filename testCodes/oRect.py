
from optimization.positioning import center_top
from pygame import Surface
from time import time
from random import randint

s = Surface((10, 10))

start = time()

for j in range(1000):
    x = randint(-100, 200)
    for i in range(10000):
        s.get_rect(centerx=x, top=x)

print("Pygame Positioning:", time() - start, "sec")

start = time()

for j in range(1000):
    x = randint(-100, 200)
    for i in range(10000):
        center_top(x, x, s.get_size())

print("Optimized Positioning:", time() - start, "sec")
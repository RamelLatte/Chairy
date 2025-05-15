

from pygame import Rect
from time import time
from random import randint
from Component import Component
from oldComponent import oldComponent

r = Rect(100, 100, 1000, 1000)

start = time()

for j in range(20000000):
    r.collidepoint(250, 250)

print("순수 파이썬:", time() - start, "sec")

comp = Component(100, 100, 5000, 5000)
comp.newMouseFields(1)
comp.setMouseField(0, 0, 0, 1000, 1000)

start = time()

for j in range(20000000):
    comp.collidepoint(0, (250, 250))

print("Cython 통합:", time() - start, "sec")
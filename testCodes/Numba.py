
from numba import jit
from time import time


@jit(nopython=True, cache=True)
def CalculateOffset(prior: int, now: int):
    if abs(prior - now) > 2:
        return now * 0.008
    
def CalculateOffset_(prior: int, now: int):
    if abs(prior - now) > 2:
        return now * 0.008


start = time()    

CalculateOffset(17, 17)

print("Compile:", time() - start, "sec")

start = time()

for i in range(10000000):
    CalculateOffset(17, 17)

print("Compiled Function:", time() - start, "sec")

start = time()

for i in range(10000000):
    CalculateOffset_(17, 17)

print("Python Function:", time() - start, "sec")
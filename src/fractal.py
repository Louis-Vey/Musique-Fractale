from typing import *
import numpy as np

def mandelbrot(z, c):
    return z ** 2 + c

def burningShip(z: complex, c: complex):
    return complex(np.abs(z.real), np.abs(z.imag)) ** 2 + c

# zoom = 1 means 1 unit per pixel
def fractalData(screenSize: Tuple[int], center: complex, zoom: float, limit: int, fn: Callable[[complex, complex], complex]):
    data = np.zeros((screenSize[0], screenSize[1]), dtype=np.uint8)

    shift = complex(screenSize[0] * zoom / 2, screenSize[1] * zoom / 2)
    for x in range(screenSize[0]):
        for y in range(screenSize[1]):
            c = complex(x * zoom, y * zoom) - shift + center
            z, i = c, 0
            while i < limit and z.real ** 2 + z.imag ** 2 < 4:
                z = fn(z, c)
                i += 1
            data[x, y] = i

    return data
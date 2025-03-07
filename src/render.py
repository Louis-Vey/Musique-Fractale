import numpy as np
from typing import *

def colorData(screenSize: Tuple[int], fractalData, limit: int):
    data = np.zeros((screenSize[0], screenSize[1], 3), dtype=np.uint8)

    for x in range(screenSize[0]):
        for y in range(screenSize[1]):
            i = fractalData[x, y]
            if i == limit:
                data[x, y] = (0, 0, 0)
            else:
                data[x, y] = (i / limit * 255, i / limit * 100, 0)

    return data

def colorDataShifted(screenSize: Tuple[int], shift: complex, zoom: float, fractalData, limit: int):
    data = np.zeros((screenSize[0], screenSize[1], 3), dtype=np.uint8)

    for x in range(screenSize[0]):
        for y in range(screenSize[1]):
            i = fractalData[x, y]
            if i == limit:
                data[x, y] = (0, 0, 0)
            else:
                data[x, y] = (i / limit * 255, i / limit * 100, 0)

    return data
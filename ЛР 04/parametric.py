import numpy as np
from math import sin, cos, radians, pi
import util

def parcircle(xc, yc, r):
    pixels = []
    step = 1 / r

    for t in np.arange(0, pi / 4 + step, step):
        x = xc + r * cos(t)
        y = yc + r * sin(t)
        util.tmirrored(pixels, x, y, xc, yc)

    return pixels


def parellipse(xc, yc, rx, ry):
    pixels = []
    step = 1 / rx if rx > ry else 1 / ry

    for t in np.arange(0, pi / 2 + step, step):
        x = xc + rx * cos(t)
        y = yc + ry * sin(t)
        util.dmirrored(pixels, x, y, xc, yc)

    return pixels

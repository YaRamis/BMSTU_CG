from math import sqrt
import util


def cancircle(xc, yc, r):
    pixels = []

    for x in range(int(xc), int(xc + int(r / sqrt(2)) + 1)):
        y = sqrt(r**2 - (x - xc)**2) + yc
        util.tmirrored(pixels, x, y, xc, yc)

    return pixels


def canellipse(xc, yc, rx, ry):
    pixels = []
    limit = int(xc + rx / sqrt(1 + ry**2 / rx**2))

    for x in range(int(xc), limit + 1):
        y = sqrt(rx**2 * ry**2 - (x - xc)**2 * ry**2) / rx + yc
        util.dmirrored(pixels, x, y, xc, yc)

    limit = int(yc + ry / sqrt(1 + rx**2 / ry**2))

    for y in range(limit, int(yc) - 1, -1):
        x = sqrt(rx**2 * ry**2 - (y - yc)**2 * rx**2) / ry + xc
        util.dmirrored(pixels, x, y, xc, yc,)

    return pixels

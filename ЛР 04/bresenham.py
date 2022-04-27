import util

def brescircle(xc, yc, r):
    pixels = []
    x = 0
    y = r
    delta = 2 * (1 - r)

    util.tmirrored(pixels, x + xc, y + yc, xc, yc)

    while x < y:
        if delta <= 0:
            delta_temp = 2 * (delta + y) - 1
            x += 1
            if delta_temp >= 0:
                delta += 2 * (x - y + 1)
                y -= 1
            else:
                delta += 2 * x + 1

        else:
            delta_temp = 2 * (delta - x) - 1
            y -= 1
            if delta_temp < 0:
                delta += 2 * (x - y + 1)
                x += 1
            else:
                delta -= 2 * y - 1

        util.tmirrored(pixels, x + xc, y + yc, xc, yc)

    return pixels


def bresellipse(xc, yc, rx, ry):
    pixels = []
    x = 0
    y = ry
    delta = ry**2 - rx**2 * (2 * ry + 1)

    util.dmirrored(pixels, x + xc, y + yc, xc, yc)

    while y > 0:
        if delta <= 0:
            delta_temp = 2 * delta + rx**2 * (2 * y - 1)
            x += 1
            delta += ry**2 * (2 * x + 1)
            if delta_temp >= 0:
                y -= 1
                delta += rx**2 * (-2 * y + 1)

        else:
            delta_temp = 2 * delta + ry**2 * (-2 * x - 1)
            y -= 1
            delta += rx**2 * (-2 * y + 1)
            if delta_temp < 0:
                x += 1
                delta += ry**2 * (2 * x + 1)

        util.dmirrored(pixels, x + xc, y + yc, xc, yc)

    return pixels

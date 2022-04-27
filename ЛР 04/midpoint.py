import util

def midpcircle(xc, yc, r):
    pixels = []
    x = r
    y = 0

    util.tmirrored(pixels, x + xc, y + yc, xc, yc)
    delta = 1 - r

    while x > y:
        y += 1
        if delta > 0:
            x -= 1
            delta -= 2 * x - 2
        delta += 2 * y + 3
        util.tmirrored(pixels, x + xc, y + yc, xc, yc)

    return pixels


def midpellipse(xc, yc, rx, ry):
    pixels = []
    x = 0
    y = ry

    delta = ry**2 - rx**2 * ry + 0.25 * rx * rx
    dx = 2 * ry**2 * x
    dy = 2 * rx**2 * y

    while dx < dy:
        util.dmirrored(pixels, x + xc, y + yc, xc, yc)

        x += 1
        dx += 2 * ry**2

        if delta >= 0:
            y -= 1
            dy -= 2 * rx**2
            delta -= dy

        delta += dx + ry**2

    delta = ry**2 * (x + 0.5)**2 + rx**2 * (y - 1)**2 - rx**2 * ry**2

    while y >= 0:
        util.dmirrored(pixels, x + xc, y + yc, xc, yc)

        y -= 1
        dy -= 2 * rx**2

        if delta <= 0:
            x += 1
            dx += 2 * ry**2
            delta += dx

        delta -= dy - rx**2

    return pixels

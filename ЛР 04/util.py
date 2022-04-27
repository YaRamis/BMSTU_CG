def tmirrored(pixels, x, y, xc, yc):
    pixels.extend([
        [x, y],
        [2*xc-x, y],
        [x, 2*yc-y],
        [2*xc-x, 2*yc-y],
        [y + xc - yc, x + yc - xc],
        [-y + xc + yc, x + yc - xc],
        [y + xc - yc, -x + yc + xc],
        [-y + xc + yc, -x + yc + xc]
    ])


def dmirrored(pixels, x, y, xc, yc):
    pixels.extend([
        [x, y],
        [2*xc-x, y],
        [x, 2*yc-y],
        [2*xc-x, 2*yc-y]
    ])

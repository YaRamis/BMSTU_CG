import matplotlib.pyplot as plt
import pylab
from numpy import sign
import math

def dda_checkStepping(xb, yb, xe, ye):
    steps = 0
    dx = xe - xb
    dy = ye - yb
    l = abs(dy)
    if abs(dx) > abs(dy):
        l = abs(dx)
    dx = dx / l
    dy = dy / l
    x = float(xb)
    y = float(yb)
    for _ in range(int(l)):
        x = x + dx
        y = y + dy
        if int(x) != int(xb) and int(y) != int(yb):
            steps = steps + 1
            xb, yb = x, y
    return steps

def bresenham_int_checkStepping(xb, yb, xe, ye):
    steps = 0
    x = xb
    y = yb
    dx = xe - xb
    dy = ye - yb
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        tmp = dx
        dx = dy
        dy = tmp
    m = dy / dx
    e = m - 0.5
    for i in range(1, int(dx + 1)):
        if e >= 0:
            if change_flag == 0:
                y = y + sy
            else:
                x = x + sx
            e = e - 1
        if change_flag == 0:
            x = x + sx
        else:
            y = y + sy
        e = e + m
        if int(x) != int(xb) and int(y) != int(yb):
            steps = steps + 1
            xb, yb = x, y
    return steps

def bresenham_float_checkStepping(xb, yb, xe, ye):
    steps = 0
    x = xb
    y = yb
    dx = xe - xb
    dy = ye - yb
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        tmp = dx
        dx = dy
        dy = tmp
    e = 2 * dy - dx
    for _ in range(1, int(dx + 1)):
        if e >= 0:
            if change_flag == 0:
                y = y + sy
            else:
                x = x + sx
            e = e - 2 * dx
        if change_flag == 0:
            x = x + sx
        else:
            y = y + sy
        e = e + 2 * dy
        if int(x) != int(xb) and int(y) != int(yb):
            steps = steps + 1
            xb, yb = x, y
    return steps

def bresenham_stepping_checkStepping(xb, yb, xe, ye):
    steps = 0
    dx = xe - xb
    dy = ye - yb
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        dx, dy = dy, dx
    m = dy / dx
    e = 1 / 2
    x = xb
    y = yb
    w = 1 - m
    for _ in range(1, int(dx)):
        if e < w:
            if change_flag == 0:
                x = x + sx
            else:
                y = y + sy
            e = e + m
        else:
            x = x + sx
            y = y + sy
            e = e - w
        if int(x) != int(xb) and int(y) != int(yb):
            steps = steps + 1
            xb, yb = x, y
    return steps

def wu_checkStepping(xb, yb, xe, ye):
    steps = 0
    x = xb
    y = yb
    dx = xe - xb
    dy = ye - yb
    sx = 1 if dx == 0 else int(sign(dx))
    sy = 1 if dy == 0 else int(sign(dy))
    dx = abs(dx)
    dy = abs(dy)
    change_flag = 0
    if dx <= dy:
        change_flag = 1
        tmp = dx
        dx = dy
        dy = tmp

    m = dy / dx
    e = -1
    if not change_flag:
        for _ in range(int(dx)):
            e += m
            if e >= 0:
                y += sy
                e -= 1
            x += sx
            if int(y) != int(yb):
                steps = steps + 1
                yb = y
    else:
        for _ in range(int(dx)):
            e += m
            if e >= 0:
                x += sx
                e -= 1
            y += sy
            if int(x) != int(xb):
                steps = steps + 1
                xb = x
    return steps

def check_stepping():
    xb = 0
    yb = 0
    all_degrees = []
    for i in range(46):
        all_degrees.append(i)
    
    all_steps = []
    steps = 0
    xe = xb + 1000
    ye = yb
    ang = 0
    while ang <= 45:
        for _ in range(100):
            steps = steps + dda_checkStepping(xb, yb, xe, ye)
        steps = steps / 100
        all_steps.append(steps)
        ang = ang + 1
        xe = int(xb + 1000 * math.cos(math.radians(ang)))
        ye = int(yb - 1000 * math.sin(math.radians(ang)))
    pylab.subplot(3, 2, 1)
    pylab.bar(all_degrees, all_steps)
    pylab.title('ЦДА')
    
    all_steps = []
    steps = 0
    xe = xb + 1000
    ye = yb
    ang = 0
    while ang <= 45:
        for _ in range(100):
            steps = steps + bresenham_float_checkStepping(xb, yb, xe, ye)
        steps = steps / 100
        all_steps.append(steps)
        ang = ang + 1
        xe = int(xb + 1000 * math.cos(math.radians(ang)))
        ye = int(yb - 1000 * math.sin(math.radians(ang)))
    pylab.subplot(3, 2, 2)
    pylab.bar(all_degrees, all_steps)
    pylab.title('Брезенхем float')
    
    all_steps = []
    steps = 0
    xe = xb + 1000
    ye = yb
    ang = 0
    while ang <= 45:
        for _ in range(100):
            steps = steps + bresenham_int_checkStepping(xb, yb, xe, ye)
        steps = steps / 100
        all_steps.append(steps)
        ang = ang + 1
        xe = int(xb + 1000 * math.cos(math.radians(ang)))
        ye = int(yb - 1000 * math.sin(math.radians(ang)))
    pylab.subplot(3, 2, 3)
    pylab.bar(all_degrees, all_steps)
    pylab.title('Брезенхем int')
    
    all_steps = []
    steps = 0
    xe = xb + 1000
    ye = yb
    ang = 0
    while ang <= 45:
        for _ in range(100):
            steps = steps + bresenham_stepping_checkStepping(xb, yb, xe, ye)
        steps = steps / 100
        all_steps.append(steps)
        ang = ang + 1
        xe = int(xb + 1000 * math.cos(math.radians(ang)))
        ye = int(yb - 1000 * math.sin(math.radians(ang)))
    pylab.subplot(3, 2, 4)
    pylab.bar(all_degrees, all_steps)
    pylab.title('Брезенхем smooth')
    
    all_steps = []
    steps = 0
    xe = xb + 1000
    ye = yb
    ang = 0
    while ang <= 45:
        for _ in range(100):
            steps = steps + wu_checkStepping(xb, yb, xe, ye)
        steps = steps / 100
        all_steps.append(steps)
        ang = ang + 1
        xe = int(xb + 1000 * math.cos(math.radians(ang)))
        ye = int(yb - 1000 * math.sin(math.radians(ang)))
    pylab.subplot(3, 2, 5)
    pylab.bar(all_degrees, all_steps)
    pylab.title('ВУ')

    pylab.show()

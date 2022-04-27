from cProfile import label
import time
import matplotlib.pyplot as plt
import pylab
import canonical
import bresenham
import midpoint
import parametric

def cmp_time():
    all_r = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    
    pylab.subplot(1, 2, 1)
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            canonical.cancircle(0, 0, r)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Каноническое уравнение')
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            parametric.parcircle(0, 0, r)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Параметрическое уравнение')
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            bresenham.brescircle(0, 0, r)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Брезенхем')
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            midpoint.midpcircle(0, 0, r)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Алгоритм средней точки')
    pylab.title('Окружность')
    pylab.xlabel('Радиус')
    pylab.ylabel('Время')
    pylab.legend()

    pylab.subplot(1, 2, 2)
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            canonical.canellipse(0, 0, r, r / 2)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Каноническое уравнение')
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            parametric.parellipse(0, 0, r, r / 2)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Параметрическое уравнение')
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            bresenham.bresellipse(0, 0, r, r / 2)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Брезенхем')
    all_time = []
    for r in all_r:
        d_time = 0
        for _ in range(20):
            start_time = time.time()
            midpoint.midpellipse(0, 0, r, r / 2)
            d_time = d_time + (time.time() - start_time)
        d_time = d_time / 20
        all_time.append(d_time)
    pylab.plot(all_r, all_time, label='Алгоритм средней точки')
    pylab.title('Эллипс')
    pylab.xlabel('Радиус')
    pylab.ylabel('Время')

    pylab.legend()
    pylab.show()

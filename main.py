import matplotlib.pyplot as plt
import math
import numpy

DELTA_TIME = 0.1 # s
A = 10
dx = 0.01

def read_input():
    return {}

def psi(a, n, x, t):
    return a*math.sin(n*math.pi*x/A)


def main():
    data = read_input()
    plt.plot([0,0], [-10,10], 'k-')
    plt.plot([A,A], [-10,10], 'k-')
    duration=100
    x = numpy.linspace(0, A, int(A/dx))
    myPlot, = plt.plot(x, [0 for _ in range(len(x))])
    for i in range(duration):
        myPlot.set_ydata([psi(A,3,x,0) for x in x])
        plt.draw()
        plt.pause(DELTA_TIME)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

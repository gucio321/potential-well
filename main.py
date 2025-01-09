#!/usr/bin/env python3
import time
import timeit

import matplotlib.pyplot as plt
import math
import numpy
import dearpygui.dearpygui as imgui
import asyncio
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

DELTA_TIME = 60 # ms
A = 10
dx = 0.01

class PotentialWellSymulator:
    def __init__(self):
        self.__WINDOW_SIZE = (800, 600)
        self.__IMG_SIZE = (400, 400)
        self.__IMG_DATA = [1.0,1.0,1.0,1.0] * self.__IMG_SIZE[0] * self.__IMG_SIZE[1]
        self.__DPI = 100

        self.x = numpy.linspace(0, A, int(A/dx))
        self.n = 1
        self.time = 0

    def run(self):
        """
        run handles UI things. Should be called once per class instance (even once per script).

        :return:
        """

        # set  up imgui context
        imgui.create_context()
        imgui.create_viewport(title='Custom Title', width=self.__WINDOW_SIZE[0], height=self.__WINDOW_SIZE[1])
        self.render()
        imgui.setup_dearpygui()
        imgui.show_viewport()
        imgui.start_dearpygui()
        imgui.destroy_context()

    def render(self):
        self.time += imgui.get_delta_time()
        with imgui.window(label="Tutorial", no_move=True, no_title_bar=True, no_collapse=True, no_scrollbar=True,no_resize=True):
            with imgui.plot(label="Symulacja", width=self.__IMG_SIZE[0], height=self.__IMG_SIZE[1]):
                self.plot()

            imgui.add_slider_int(label="n", max_value=10, callback=lambda _,value : self._set_n(value))

    def plot(self):
        """
        plot is supposed to update plot texture to the atlas.
        :return:
        """
        imgui.add_plot_axis(imgui.mvXAxis, label="x")
        imgui.add_plot_axis(imgui.mvYAxis,label="y", tag="y_axis")
        imgui.add_line_series([0,0], [-10,10], parent="y_axis")
        imgui.add_line_series([A,A], [-10,10], parent="y_axis")
        imgui.add_line_series(self.x, [psi(1, self.n, X, self.time) for X in self.x], parent="y_axis")

    def _set_n(self, n):
        self.n = n

def psi(a, n, x, t):
    return a*math.sin(n*math.pi*x/A)

    # duration=100
    # x = numpy.linspace(0, A, int(A/dx))
    # myPlot, = plt.plot(x, [0 for _ in range(len(x))])
    # for i in range(duration):
    #     myPlot.set_ydata([psi(A,3,x,i*DELTA_TIME) for x in x])
    #     plt.draw()
    #     plt.pause(DELTA_TIME)

def main():
    sim = PotentialWellSymulator()
    sim.run()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

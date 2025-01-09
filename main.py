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
        self.__IMG_SIZE = (600, 600)
        self.__IMG_DATA = [1.0,1.0,1.0,1.0] * self.__IMG_SIZE[0] * self.__IMG_SIZE[1]
        self.__DPI = 100

        self.x = numpy.linspace(0, A, int(A/dx))
        self.time = 0

    def run(self):
        """
        run handles UI things. Should be called once per class instance (even once per script).

        :return:
        """

        # set  up imgui context
        imgui.create_context()

        # register plot texture
        with imgui.texture_registry(show=False): # change to true for debugging
            imgui.add_dynamic_texture(width=self.__IMG_SIZE[0], height=self.__IMG_SIZE[1], default_value=self.__IMG_DATA, tag="texture_tag")

        self.render()
        imgui.create_viewport(title='Custom Title', width=self.__WINDOW_SIZE[0], height=self.__WINDOW_SIZE[1])
        imgui.setup_dearpygui()
        imgui.show_viewport()
        while imgui.is_dearpygui_running():
            self.render()
            self.plot()
            imgui.render_dearpygui_frame()
        imgui.destroy_context()

    def render(self):
        with imgui.window(label="Tutorial", no_move=True, no_title_bar=True, no_collapse=True, no_scrollbar=True,no_resize=True):
            imgui.add_image("texture_tag")
            # imgui.add_color_picker((255, 0, 255, 255), label="Texture",
            #                  no_side_preview=True, alpha_bar=True, width=200, callback=_update_dynamic_textures)

    def plot(self):
        """
        plot is supposed to update plot texture to the atlas.
        :return:
        """
        fig = plt.figure(figsize=(self.__IMG_SIZE[0]/self.__DPI, self.__IMG_SIZE[1]/self.__DPI))

        # do plotting
        plt.plot([0,0], [-10,10], 'k-')
        plt.plot([A,A], [-10,10], 'k-')
        self.time += imgui.get_delta_time()
        # plt.plot(self.x,[psi(A,3,x,self.time) for x in self.x])

        # now a bit of python magic to export figure to imgui texture
        canvas = FigureCanvas(fig)
        plt.close(fig)
        canvas.draw()
        h,w = canvas.get_width_height()
        image = numpy.frombuffer(canvas.tostring_argb(), dtype=numpy.uint8)
        image.reshape((h,w,4)) # make it ARGB format
        # ARGB => RGBA
        image = numpy.array(image).reshape(-1, 4)[:, [1,2,3,0]].flatten()
        # push to registry
        imgui.set_value("texture_tag", image)

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

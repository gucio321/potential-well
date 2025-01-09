#!/usr/bin/env python3
import time
import timeit

import matplotlib.pyplot as plt
import math
import numpy
import dearpygui.dearpygui as imgui
import asyncio

DELTA_TIME = 60 # ms
A = 10
dx = 0.01

class PotentialWellSymulator:
    def __init__(self):
        self.__WINDOW_SIZE = (800, 600)
        self.__IMG_SIZE = (600, 600)
        self.__IMG_DATA = [1.0,1.0,1.0,1.0] * self.__IMG_SIZE[0] * self.__IMG_SIZE[1]

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

# def _update_dynamic_textures(sender, app_data, user_data):
#     new_color = imgui.get_value(sender)
#     new_color[0] = new_color[0] / 255
#     new_color[1] = new_color[1] / 255
#     new_color[2] = new_color[2] / 255
#     new_color[3] = new_color[3] / 255
#
#     new_texture_data = []
#     for i in range(0, 100 * 100):
#         new_texture_data.append(new_color[0])
#         new_texture_data.append(new_color[1])
#         new_texture_data.append(new_color[2])
#         new_texture_data.append(new_color[3])
#
#     imgui.set_value("texture_tag", new_texture_data)



# def psi(a, n, x, t):
#     return a*math.sin(n*math.pi*x/A)
#
# def main():
#     running=True
#     screen = pygame.display.set_mode((800,600))
#     clock = pygame.time.Clock()
#     fig, ax = plt.subplot(dpi=100)
#     while running:
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT:
#                 running = False
#
#         screen.fill('red')
#
#
#         pygame.display.flip() # tell it to actually render?
#         clock.tick(DELTA_TIME)
#
#     pygame.quit()
#
#     plt.plot([0,0], [-10,10], 'k-')
#     plt.plot([A,A], [-10,10], 'k-')
#     duration=100
#     x = numpy.linspace(0, A, int(A/dx))
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

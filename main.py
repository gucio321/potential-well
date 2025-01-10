#!/usr/bin/env python3
import math
import numpy
import dearpygui.dearpygui as imgui

class PotentialWellSymulator:
    def __init__(self):
        self.__WINDOW_SIZE = (800, 600)
        self.__TITLE = "Potential Well Simulation"
        self.__PRIMARY_WINDOW_ID = 'Primary Window' # this will be hidden as title bar is hidden.
        self.__IMG_SIZE = (400, 400)
        self.__A_SLIDER_ID = "a_slider_id"
        self.dx = 0.01 # sets plotting accuracy (the higher the smoother plot is and more resources are used)

        self._a = 0
        self.x = []
        self.n = 1
        self.time = 0

    def __initialize(self):
        self.a = 10

    def run(self):
        """
        run handles UI things. Should be called once per class instance (even once per script).

        :return:
        """

        # set  up imgui context
        imgui.create_context()
        imgui.create_viewport(title='Custom Title', width=self.__WINDOW_SIZE[0], height=self.__WINDOW_SIZE[1])
        self.render()
        self.__initialize()
        imgui.setup_dearpygui()
        imgui.show_viewport()
        imgui.set_primary_window(self.__PRIMARY_WINDOW_ID, True)
        imgui.start_dearpygui()
        imgui.destroy_context()

    def render(self):
        self.time += imgui.get_delta_time()
        with imgui.window(tag=self.__PRIMARY_WINDOW_ID, no_move=True, no_title_bar=True, no_collapse=True, no_scrollbar=True,no_resize=True):
            with imgui.plot(label="Symulacja", width=self.__IMG_SIZE[0], height=self.__IMG_SIZE[1]):
                imgui.add_plot_axis(imgui.mvXAxis, label="x")
                imgui.add_plot_axis(imgui.mvYAxis, label="y", tag="y_axis")

                # initialize plots
                imgui.add_line_series([], [], tag='left_wall', parent='y_axis')
                imgui.add_line_series([], [], tag='right_wall', parent='y_axis')
                imgui.add_line_series([], [], tag='psi', parent='y_axis')

                # first ploting iteration
                self.plot()

            imgui.add_slider_int(label="n",default_value=self.n, max_value=10, callback=lambda _,value : self._set_n(value))
            imgui.add_input_int(tag=self.__A_SLIDER_ID, label="Szerokość studni A", default_value=self.a, callback=lambda _, value: self.__set_a(value))

    def plot(self):
        """
        plot is supposed to update plot texture to the atlas.
        :return:
        """
        imgui.set_value('left_wall', [[0,0], [-10,10]])
        imgui.set_value('right_wall',[[self.a,self.a], [-10,10]])
        imgui.set_value('psi', [self.x, [self.psi(1, self.n, X, self.time) for X in self.x]])

    def _set_n(self, n):
        self.n = n
        self.plot() # replot

    def __set_a(self, a):
        self.a = a

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, new_a):
        self._a = new_a
        self.x = numpy.linspace(0, new_a, int(new_a/self.dx))
        self.plot()
        imgui.set_value(self.__A_SLIDER_ID, new_a)

    def psi(self, a, n, x, t):
        return a*math.sin(n*math.pi*x/self.a)

def main():
    sim = PotentialWellSymulator()
    sim.run()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

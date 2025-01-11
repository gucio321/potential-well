#!/usr/bin/env python3
import math
import numpy
import dearpygui.dearpygui as imgui
from scipy import constants as const

POLISH_CHARS = 'ąćęłńóśżź'
POLISH_CHARS += POLISH_CHARS.upper()

class PotentialWellSymulator:
    def __init__(self):
        self.__WINDOW_SIZE = (800, 600)
        self.__TITLE = "Potential Well Simulation"
        self.__PRIMARY_WINDOW_ID = 'Primary Window' # this will be hidden as title bar is hidden.
        self.__IMG_SIZE = (-1, 400)
        self.__W_SLIDER_ID = "width_slider_id"
        self.__TIME_COUNTER_ID = "time_counter"
        self.dx = 0.001 # sets plotting accuracy (the higher the smoother plot is and more resources are used)
        self.tscale = 1

        self._width = 0
        self.x = []
        self.n = 1
        self._time = 0
        self.mass = 1
        self.width = 10
        self.N = 10**4

    def run(self):
        """
        run handles UI things. Should be called once per class instance (even once per script).

        :return:
        """

        # set  up imgui context
        imgui.create_context()
        with imgui.font_registry():
            with imgui.font('./fonts/NotoSans-Regular.ttf', 22) as font:
                imgui.add_font_range_hint(imgui.mvFontRangeHint_Default)
                imgui.add_font_chars([ord(c) for c in POLISH_CHARS])
        imgui.create_viewport(title='Custom Title', width=self.__WINDOW_SIZE[0], height=self.__WINDOW_SIZE[1])
        self.render()
        # imgui.bind_font(default_font)
        imgui.bind_font(font)
        imgui.setup_dearpygui()
        imgui.show_viewport()
        imgui.set_primary_window(self.__PRIMARY_WINDOW_ID, True)
        while imgui.is_dearpygui_running():
            self.time += imgui.get_delta_time()
            self.plot()
            imgui.render_dearpygui_frame()
        imgui.destroy_context()

    def render(self):
        with imgui.window(tag=self.__PRIMARY_WINDOW_ID, no_move=True, no_title_bar=True, no_collapse=True, no_scrollbar=True,no_resize=True):
            with imgui.tab_bar():
                with imgui.tab(label="wykres"):
                    with imgui.plot(label="Symulacja", width=self.__IMG_SIZE[0], height=self.__IMG_SIZE[1]):
                        imgui.add_plot_axis(imgui.mvXAxis, label="Położenie")
                        imgui.add_plot_axis(imgui.mvYAxis, label="Energia", tag="y_axis")

                        # initialize plots
                        imgui.add_line_series([], [], tag='left_wall', parent='y_axis')
                        imgui.add_line_series([], [], tag='right_wall', parent='y_axis')
                        imgui.add_line_series([], [], tag='psi', parent='y_axis')
                        imgui.add_line_series([], [], tag='psi1', parent='y_axis')
                        imgui.add_line_series([], [], tag='psi2', parent='y_axis')

                        # first ploting iteration
                        self.plot()

                    with imgui.group(horizontal=True):
                        imgui.add_text("", tag=self.__TIME_COUNTER_ID)
                        imgui.add_slider_float(label="Skala czasu", default_value=self.tscale, min_value=0, max_value=2,
                                           callback=lambda _, v: self._set_tscale(v))
                with imgui.tab(label="Symulacja MC"):
                    with imgui.plot():
                        imgui.add_plot_axis(imgui.mvXAxis, label="położenie")
                        imgui.add_plot_axis(imgui.mvYAxis, label="Ilość pomiarów w przedziale", tag="hist_y")
                        imgui.add_histogram_series([], parent='hist_y')
                    imgui.add_button(label="Odpalaj")
                    imgui.add_input_int(label="Liczba symulacji Monte Carlo", callback=lambda _, v : self._set_N(v))

            imgui.add_slider_int(label="n",tag='n_slider', default_value=self.n, max_value=10, callback=lambda _,value : self._set_n(value))
            with imgui.tooltip('n_slider'):
                imgui.add_text('''N określa poziom energetyczny cząstki w studni.''')
            imgui.add_drag_float(tag=self.__W_SLIDER_ID,speed=0.05, label="Szerokość studni A", default_value=self.width, callback=lambda _, value: self.__set_w(value))
            imgui.add_input_float(label="masa [mas elektornu]", default_value=self.mass, callback=lambda _, v:self._set_m(v))


    def plot(self):
        """
        plot is supposed to update plot texture to the atlas.
        :return:
        """
        imgui.set_value('left_wall', [[0,0], [-10,10]])
        imgui.set_value('right_wall',[[self.width,self.width], [-10,10]])
        imgui.set_value('psi', [self.x, [self.psi(self.E(self.mass*const.m_e,self.width,self.n),self.width, self.n, X, self.time * self.tscale) for X in self.x]])
        imgui.set_value('psi1', [self.x, [self.psi1(self.E(self.mass*const.m_e,self.width,self.n),self.width, self.n, X, self.time * self.tscale) for X in self.x]])
        imgui.set_value('psi2', [self.x, [self.psi2(self.E(self.mass*const.m_e,self.width,self.n),self.width, self.n, X, self.time * self.tscale) for X in self.x]])

    def _set_n(self, n):
        self.n = n
        self.plot() # replot

    def __set_w(self, w):
        self.width = w
    def _set_tscale(self, t):
        self.tscale = t
    def _set_m(self,m):
        if m == 0: # We are not ready to return yet imo
            return
    def _set_N(self, N):
        self.N = N

        self.mass = m

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        self._width = w
        self.x = numpy.linspace(0, w, int(w/self.dx))
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, t):
        self._time = t
        imgui.set_value(self.__TIME_COUNTER_ID, f'Czas = {t*self.tscale:.1f} s')

    @staticmethod
    def psi(E, L, n, x, t):
        return 2/L * math.sin(n*math.pi*x/L)**2

    def psi1(self, E, L, n, x, t):
        return math.cos(-E / const.hbar * t) ** 2 * self.psi(E, L, n, x, t)

    def psi2(self, E, L, n, x, t):
        return math.sin(-E / const.hbar * t) ** 2 * self.psi(E, L, n, x, t)

    @staticmethod
    def E(m,L,n):
        return n**2*math.pi**2*const.hbar**2/(2*m*L**2)


def main():
    sim = PotentialWellSymulator()
    sim.run()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

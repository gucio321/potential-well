#!/usr/bin/env python3
import numpy
import dearpygui.dearpygui as imgui
from scipy import constants as const
from schrodinger import schrodinger as schrodinger
import scipy.constants as constants
import scipy.stats as stats

POLISH_CHARS = 'ąćęłńóśżź'
POLISH_CHARS += POLISH_CHARS.upper()

class PotentialWellSymulator:
    def __init__(self):
        # constants - should not be changed by program.
        self.__WINDOW_SIZE = (800, 600) # main window's size
        self.__TITLE = "Potential Well Simulation" # window title
        self.__PRIMARY_WINDOW_ID = 'Primary Window' # this will be hidden as title bar is hidden.
        self.__IMG_SIZE = (-1, 400) # size for our plots. -1 means auto-fill available space
        self.__TIME_COUNTER_ID = "time_counter"
        self.dx = 0.001 # sets plotting accuracy (the higher the smoother plot is and more resources are used)
        self.tscale = 1

        self.schrodinger = schrodinger()

        self.n = 5
        self._width = 0
        self.x = []
        self._time = 0
        self._mass = 0.005
        self._V0 = 100 # V0 is % of current E
        self._width = 10
        self.__update_x()

        # Monte Carlo stuff
        # the idea behind this is as follows:
        # - when is_running;
        # - every frame (while loop below) rollls_per_sec random numbers is generated
        # - they are added to hist_data and histogram is updated as well.
        # - if rolls_progress hits N, is_running is set to False and probably everything else is reset as well
        self.N = 10**4 # number of rolls
        self.hist_data = []
        self.is_running = False
        self.rolls_per_frame = 10
        self.rolls_progress = 0

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
            self.plot_histogram()
            self.update_hist()
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
                    with imgui.plot(width=self.__IMG_SIZE[0], height=self.__IMG_SIZE[1]):
                        imgui.add_plot_axis(imgui.mvXAxis, label="położenie", auto_fit=True)
                        imgui.add_plot_axis(imgui.mvYAxis, label="Ilość pomiarów w przedziale", tag="hist_y", auto_fit=True)
                        imgui.add_histogram_series([], parent='hist_y', tag='hist', bar_scale=1/self.N)
                    imgui.add_progress_bar(default_value=0, tag='progress')
                    imgui.add_button(label="Start", tag='odpalaj_btn', callback=lambda: self._set_is_running())
                    imgui.add_input_int(label="Liczba symulacji Monte Carlo", default_value=self.N, callback=lambda _, v : self._set_N(v))
                    imgui.add_input_int(label="Liczba symulacji na klatkę", default_value=self.rolls_per_frame, callback=lambda _, v: self._set_rpf(v), tag='rpf')
                    with imgui.tooltip('rpf'):
                        imgui.add_text(f"Co klatkę zostanie wykonanych dokładnie {self.rolls_per_frame} symulacji które zostaną naniesione poywższy histogram.\nNadmierne zwiększenie wartości możen wpłynąć na wydjaność!")

            imgui.add_slider_int(label="n",tag='n_slider', default_value=self.n, max_value=10, callback=lambda _,value : self._set_n(value))
            with imgui.tooltip('n_slider'):
                imgui.add_text('''N określa poziom energetyczny cząstki w studni.''')
            imgui.add_drag_float(speed=0.05, label="Szerokość studni A", default_value=self.width, callback=lambda _, value: self.__set_w(value))
            imgui.add_drag_float(label="masa [mas elektornu]", speed=0.001, default_value=self.mass, min_value=0, callback=lambda _, v:self._set_m(v))
            # max value: tested on default setup. Returns decimalError (int overflow) for 100x larger value
            imgui.add_drag_int(label="V0 [% E]", tag="v0_slider", default_value=self.V0, min_value=1, max_value=10000000000, callback=lambda _, v: self._set_v0(v))
            with imgui.tooltip('v0_slider'):
                imgui.add_text("Określa mnożnik Energii 1 poziomu energetycznego. Ponieważ z założenia V0 jest większy niż E\nta wartość mnoży energię aby uzyskać potencjał V0(mnożnik) = E1*mnożnik")

    def plot(self):
        """
        plot is supposed to update plot texture to the atlas.
        :return:
        """
        h = 4/self.width # analogy to 2/L
        imgui.set_value('left_wall', [[0,0], [-h,h]])
        imgui.set_value('right_wall',[[self.width,self.width], [-h,h]])
        m = self.mass*const.m_e
        self.Es = self.schrodinger.E(m, self.width, self.V)
        E = self.Es[self.n] if self.n < len(self.Es) else self.Es[-1]
        ys = self.schrodinger.psi(E,self.V,self.width, m, self.x, self.time)
        ys = ys.real.tolist()
        imgui.set_value('psi', [self.x, ys])

    def plot_histogram(self):
        """
        plot_histogram just updates data on histogram whenever it is called
        :return:
        """
        imgui.set_value('hist', [self.hist_data])

    def update_hist(self):
        """
        update_hist unlike plot_histogram is responsible for updating histogram DATA set (not hist itself).
        :return:
        """
        if not self.is_running:
            return

        for i in range(self.rolls_per_frame):
            if self.N == self.rolls_progress:
                self.rolls_progress = 0
                self._set_is_running()
                return

            # rejection sampling implementation
            while True:
                sample = stats.uniform.rvs(loc=-self.width/2, scale=2*self.width, size=1) # random position
                roll = stats.uniform.rvs(scale=2/self.width) # explaination: 2/width is 2/L from psi which is the maximum of psi.
                # if the following condition is met, it means we can take this sample and proceed
                print(len(self.Es))
                if roll <= self.schrodinger.psi(self.Es[self.n], self.V, self.width,self.mass, sample, 0)[0]**2:
                    print(sample, roll, self.schrodinger.psi(self.Es[self.n], self.V, self.width, self.mass, sample, 0)[0]**2)
                    self.hist_data.append(sample[0])
                    break
            self.rolls_progress += 1
            imgui.set_value('progress', self.rolls_progress/self.N)

    def _set_n(self, n):
        self.n = n
        self.plot() # replot
    def __set_w(self, w):
        self.width = w
    def _set_tscale(self, t):
        self.tscale = t
    def _set_m(self,m):
        if m == 0: # We are not ready to do things yet imo
            return
        self.mass = m
    def _set_N(self, N):
        self.N = N
    def _set_is_running(self):
        imgui.set_item_label('odpalaj_btn', "Stop") if not self.is_running else imgui.set_item_label('odpalaj_btn', "Start")
        if not self.is_running:
            self.hist_data = []
            self.rolls_progress = 0
            imgui.set_value('progress', 0)
        self.is_running = not self.is_running
    def _set_rpf(self, rpf):
        self.rolls_per_frame = rpf
    def _set_v0(self, v):
        self.V0 = v

    def __update_x(self):
        self.x = numpy.linspace(-self.width, 2 * self.width, int(self.width / self.dx))

    def __recalc_Es(self):
        self.Es = self.schrodinger.E(self.m, self.width, self.V)
        new_n = len(self.Es)
        imgui.configure_item('n_slider', max_value=new_n)
        if self.n > new_n:
            self.n = new_n
            imgui.set_value('n_slider', new_n)

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, w):
        self._width = w
        self.__update_x()
        self.__recalc_Es()

    # Properties section:
    @property
    def V(self):
        """
        As we store potential as an intager, it is EXTREMELY large.
        This is a kind of wrapper for self.V0.
        If the code refers self.V (instead of self.V0) it is like doing self.V0*1e-37
        :return: real porential value.
        """
        return self.V0 * 1e-37

    @property
    def m(self):
        """
        same as for self.V - wrapper for self.mass
        :return:  real mass
        """
        return self.mass*constants.m_e

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, t):
        self._time = t
        imgui.set_value(self.__TIME_COUNTER_ID, f'Czas = {t*self.tscale:.1f} s')

    @property
    def mass(self):
        return self._mass
    @mass.setter
    def mass(self, m):
        self._mass = m
        self.__recalc_Es()

    @property
    def V0(self):
        return self._V0
    @V0.setter
    def V0(self, v):
        self._V0 = v
        self.__recalc_Es()

def main():
    sim = PotentialWellSymulator()
    sim.run()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

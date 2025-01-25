import scipy.constants as constants
import math
import numpy as np
from scipy.integrate import simpson

class schrodinger:
    """
    Schrodinger represents finite potential well math backend.
    """

    def __init__(self):
        self._cache = {}

    @staticmethod
    # def psiModSquare(L, n, x):
    #     """
    #     psi represents a Schrodinger equation solution for Finite Potential Well problem
    #     :param L: szerokość studni (przedział od 0 do L
    #     :param n: obecny poziom energetyczny
    #     :param x: wartość dla danego x
    #     :return: zwraca rozwiązanie
    #     """
    #     return 2/L * math.sin(n*math.pi*x/L)**2
    #
    #     pass

    @staticmethod
    def E(m,L, V):
        """
        E returns well energy at the given energy level

        :param m: particle mass
        :param L: well width
        :param n: energy level
        :return: numerical value
        """
        def transcendental_eq(E):
            hbar = constants.hbar
            k = np.sqrt(2 * m * E) / hbar
            alpha = np.sqrt(2 * m * (V - E)) / hbar
            # return 2 * alpha * k * np.cos(k * L) + (alpha**2 - k**2) * np.sin(k * L)
            kL = k*L
            return (k/alpha - alpha/k)- 2*1/np.tan(kL)
        # Solve for E (initial guess based on infinite well)
        # solving this looks as follows:
        # 1. (we are in range from 0 to V because E is always less than V)
        #    Define E0 = something really smalll
        E0 = 1e-40
        dE = V/10**2
        E = [E0, E0, E0]
        Fs = [transcendental_eq(E0)] * 3
        solutions = [0]
        while True:
            if np.abs(Fs[0]) > np.abs(Fs[1]) and np.abs(Fs[2]) > np.abs(Fs[1]):
                solutions.append(E[1])
            E = E[1:] + [E[-1]+dE]
            if E[-1] >= V:
                break
            Fs = Fs[1:] + [transcendental_eq(E[-1])]

        return solutions

    def psi(self, E, V, L, m, n, x, t):
        # so lets write it from scratch.
        # 1. define substitutions I'll use later:
        hbar = constants.hbar
        k = np.sqrt(2 * m * E) / hbar
        alpha = np.sqrt(2 * m * (V - E)) / hbar
        # 2. here are schrodinger equation solutions:
        # psi1 = C*exp(alpha *x)
        # psi2 = A*sin(k*x) + B*cos(k*x)
        # psi3 = D*exp(-alpha*(x-L))
        # And here are conditions (from boundry conditions) for A,B,C and D:
        # C = B
        # alpha*C = A*k
        # A*sin(kL) + B*cos(Kl) = D
        # A*k*cos(kL) - B*k*sin(kL) = -D*alpha
        # so:
        # C = B
        # A = alpha/k * B
        # D = B*(alpha/k * sin(kL) + cos(k*L))
        # as we can see, there are only 3 equations (because the 4th is linearly dependent on 3rd).
        # The last needed equation to come up with these constants is the normalization of our psi function.
        # It could be calculated by \int_{-\infty}^{\infty} E*psi(x) dx = 1.
        # 3. assume initial vallue for e.g. C = 1:
        C = 1.0
        # 4. comput remaining constants:
        B = C
        A = (alpha / k) * B
        D = B*(alpha/k * np.sin(k*L) + np.cos(k*L))
        # Helper function to compute spatial part without recursion
        def spatial_wavefunction(x_vals):
            psi_x = np.zeros_like(x_vals, dtype=np.complex128)
            # Region I (x < 0)
            mask_I = (x_vals < 0)
            psi_x[mask_I] = C * np.exp(alpha * x_vals[mask_I])
            # Region II (0 ≤ x ≤ L)
            mask_II = (x_vals >= 0) & (x_vals <= L)
            psi_x[mask_II] = A * np.sin(k * x_vals[mask_II]) + B * np.cos(k * x_vals[mask_II])
            # Region III (x > L)
            mask_III = (x_vals > L)
            psi_x[mask_III] = D * np.exp(-alpha * (x_vals[mask_III] - L))
            return psi_x

        # Compute spatial part for input x
        psi_x = spatial_wavefunction(x)

        # Time-dependent phase
        time_phase = np.exp(-1j * E * t / hbar)
        psi_total = psi_x * time_phase

        # Compute normalization using spatial part only (no recursion)
        x_norm = np.linspace(-5 * L, 5 * L, 10000)
        psi_norm = spatial_wavefunction(x_norm)  # Use helper, NOT self.psi()
        norm = simpson(np.abs(psi_norm) ** 2, x_norm)

        # Return normalized wavefunction
        return (psi_total / np.sqrt(norm)).item() if np.isscalar(x) else psi_total / np.sqrt(norm)

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
    def psiModSquare(L, n, x):
        """
        psi represents a Schrodinger equation solution for Finite Potential Well problem
        :param L: szerokość studni (przedział od 0 do L
        :param n: obecny poziom energetyczny
        :param x: wartość dla danego x
        :return: zwraca rozwiązanie
        """
        return 2/L * math.sin(n*math.pi*x/L)**2

        pass

    @staticmethod
    def E(m,L,n):
        """
        E returns well energy at the given energy level
        :param m: particle mass
        :param L: well width
        :param n: energy level
        :return: numerical value
        """
        return n**2*math.pi**2*constants.hbar**2/(2*m*L**2)

    def count_solutions(self, m, L, V0):
        """
        count_solutions counts a number of possible energy levels at the given V0 potential.

        Here is how it works:
        - it graphical solution of the following equation: sqrt(R^2 - alpha^2) = -alpha * ctg(alpha)
        - The solution is: (n-1)^2 * A < V < n^2 * A where n is a natural number.
        - n could be calcuated by celling(sqrt(V/A))

        ref: https://youtu.be/VhNzzQpQDsw?t=2663

        :param m: mass
        :param L: well width
        :param V0: potential
        :return: number of possible energy levels
        """

        n = 1
        V = V0*self.E(m,L,1)
        A = (math.pi/2) * constants.hbar / L * math.sqrt(2/m)
        VperA = math.sqrt(V)/A
        return math.ceil(VperA)
    def psi(self, E, V, L, m, n, x, t):
        # hbar = constants.hbar
        hbar = 1.0
        m = 1.0

        # Compute k and alpha (ensure E < V)
        k = np.sqrt(2 * m * E) / hbar
        alpha = np.sqrt(2 * m * (V - E)) / hbar

        # Coefficients (B set to 1)
        B = 1.0
        A = (alpha / k) * B
        C = B
        D = A * np.sin(k * L) + B * np.cos(k * L)

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
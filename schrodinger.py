import scipy.constants as constants
import math

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

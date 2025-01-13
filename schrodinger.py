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

    def alpha(self):
        pass
    def R(self, m, L, V0):
        return math.sqrt(m*L**2*V0/constants.hbar**2)
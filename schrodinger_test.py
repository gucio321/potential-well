#!/usr/bin/env python3
import unittest
from schrodinger import schrodinger
import scipy.constants as constants

class SchrodingerTest(unittest.TestCase):
    def test_psi_random_0_on_1_value(self):
        i = schrodinger()
        m = 0.005*constants.m_e
        L = 10.
        V = 1e-37
        E = i.E(m, L, V)[1]
        x = -3.80603727
        psi = i.psi(E, V, L, m, [x], 0)
        self.assertGreater(psi, 0)

if __name__ == '__main__':
    unittest.main()
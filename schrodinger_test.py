#!/usr/bin/env python3
import unittest
import schrodinger

class SchrodingerTest(unittest.TestCase):
    def test_TestBothSidesSameSign(self):
        instance = schrodinger.schrodinger()
        m = 1
        t = 0
        V = 10**-37
        L = 10
        E = instance.E(m, L, V)
        psi0L = instance.psi(E, V, L, m, 1, [0, L], t)
        print(psi0L)

        self.assertEqual(np.abs(psi0L[0]), np.abs(psi0L[1]))

if __name__ == '__main__':
    unittest.main()
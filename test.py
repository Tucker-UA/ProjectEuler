import unittest
import primes.primes as primes
import digits.digits as digits

class TestPrimeMethods(unittest.TestCase):
    def setUp(self):
        self.maxN = 10**5
        self.P = primes.primes(self.maxN)

    def test_isprimeProbabilistic(self):
        for n in range(1,self.maxN):
            if n in self.P:
                self.assertTrue(primes.isprime(n))
            else:
                self.assertFalse(primes.isprime(n))

    def test_isprimeDeterministicMaxPrime(self):
        maxPrime = 10**3
        for n in range(1,self.maxN):
            if n in self.P:
                self.assertTrue(primes.isprime(n, method = "Best Deterministic",  maxPrime = maxPrime))
            else:
                self.assertFalse(primes.isprime(n, method = "Best Deterministic", maxPrime = maxPrime))
    
    def test_primes(self):
        self.assertEqual(primes.primes(12), [2, 3, 5, 7, 11])

if __name__ == "__main__":
    unittest.main()

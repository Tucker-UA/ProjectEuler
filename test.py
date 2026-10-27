import unittest
import primes.primes as primes
import digits.digits as digits

class TestPrimeMethods(unittest.TestCase):
    def test_isprime(self):
        maxN = 100000
        P = primes.primes(100000)
        for n in range(1,maxN):
            if n in P:
                self.assertTrue(primes.isprime(n))
            else:
                self.assertFalse(primes.isprime(n))

    def test_isprimeWithMaxPrime(self):
        maxN = 100000
        maxPrime = maxN 
        P = primes.primes(100000)
        for n in range(1,maxN):
            if n in P:
                self.assertTrue(primes.isprime(n, maxPrime = maxPrime))
            else:
                self.assertFalse(primes.isprime(n, maxPrime = maxPrime))
    
    def test_primes(self):
        self.assertEqual(primes.primes(12), [2, 3, 5, 7, 11])

if __name__ == "__main__":
    unittest.main()

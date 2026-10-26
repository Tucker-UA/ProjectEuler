import unittest
import primes.primes as primes
import digits.digits as digits

class TestPrimeMethods(unittest.TestCase):
    def test_isprime(self):
        self.assertTrue(primes.isprime(37))
        self.assertFalse(primes.isprime(35))

    def test_primes(self):
        self.assertEqual(primes.primes(12), [2, 3, 5, 7, 11])

if __name__ == "__main__":
    unittest.main()

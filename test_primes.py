import unittest
import sys
from io import StringIO
from primes import get_first_primes, get_nth_prime

class TestPrimeCLI(unittest.TestCase):
    
    def test_get_first_primes_10(self):
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        result = get_first_primes(10)
        self.assertEqual(result, expected)
    
    def test_get_first_primes_1(self):
        expected = [2]
        result = get_first_primes(1)
        self.assertEqual(result, expected)
    
    def test_get_first_primes_0(self):
        expected = []
        result = get_first_primes(0)
        self.assertEqual(result, expected)
    
    def test_get_nth_prime_10(self):
        expected = 29
        result = get_nth_prime(10)
        self.assertEqual(result, expected)
        
    def test_get_nth_prime_1(self):
        expected = 2
        result = get_nth_prime(1)
        self.assertEqual(result, expected)
        
    def test_get_nth_prime_5(self):
        expected = 11
        result = get_nth_prime(5)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
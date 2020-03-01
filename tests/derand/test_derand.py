import unittest
from ..context import cryptraider

import random

class TestBasicFunction(unittest.TestCase):
    def test_default_state(self):
        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        self.assertFalse(derand.is_state_fully_recovered())
        
    def test_not_enough_observations(self):
        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        derand.append_observed_bytes([0 for _ in range(623)])
        self.assertFalse(derand.is_state_fully_recovered())

        derand.append_observed_bytes([0])
        self.assertTrue(derand.is_state_fully_recovered())
 
    def test_simple_bytestream(self):
        N = 1000
        chunk1 = [random.getrandbits(32) for i in range(N)]
        chunk2 = [random.getrandbits(32) for i in range(N)]

        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        
        
        self.assertFalse(derand.is_state_fully_recovered())
        derand.append_observed_bytes(chunk1)

        self.assertTrue(derand.is_state_fully_recovered())
        calculated_bytes = derand.get_bytestream(len(chunk2))
        self.assertEqual(chunk2, calculated_bytes)
    
    def test_larger_bytestream(self):
        chunk1 = [random.getrandbits(32) for i in range(624)]
        chunk2 = [random.getrandbits(32) for i in range(10000)]

        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        derand.append_observed_bytes(chunk1)

        self.assertTrue(derand.is_state_fully_recovered())
        calculated_bytes = derand.get_bytestream(len(chunk2))
        self.assertEqual(chunk2, calculated_bytes)
 
if __name__ == '__main__':
    unittest.main()
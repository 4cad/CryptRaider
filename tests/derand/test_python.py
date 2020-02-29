import unittest
from ..context import cryptraider

import random

def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9d2c5680
    x ^= (x << 15) & 0xefc60000
    x ^= x >> 18
    return (x & 0xffffffff)

def unshiftLeft(x, shift, mask):
    res = x
    for _ in range(32):
        res = x ^ (res << shift & mask)
    return res

def unshiftRight(x, shift):
    res = x
    for _ in range(32):
        res = x ^ res >> shift
    return res

def untemper(x):
    x = unshiftRight(x, 18)
    x = unshiftLeft(x, 15, 0xefc60000)
    x = unshiftLeft(x, 7, 0x9d2c5680)
    x = unshiftRight(x, 11)
    return x

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
    
    def test_MT19937Simplified(self):
        seed = 0x31337

        mt = random.Random(seed)

        stream = [ mt.getrandbits(32) for x in range(2000) ]

        state_stream = [untemper(x) for x in stream]
        for i in range(1000) :
            upper = 0x80000000
            lower = 0x7fffffff

            x = ((state_stream[i] & upper) + (state_stream[i + 1] & lower)) & 0xFFFFFFFF
            twisted = state_stream[i + 397] ^ (x >> 1)

            if x & 1 != 0:
                twisted ^= 0x9908b0df
            
            self.assertEqual(twisted, state_stream[i+624])
        
        result_stream = list()
        for j in range(1000, 2000) :
            i = j-624
            x = ((state_stream[i] & upper) + (state_stream[i + 1] & lower)) & 0xFFFFFFFF
            twisted = state_stream[i + 397] ^ (x >> 1)

            if x & 1 != 0:
                twisted ^= 0x9908b0df
            
            self.assertEqual(twisted, state_stream[j])
            result_stream.append(twisted)
        self.assertEqual(result_stream, state_stream[1000:])

        incremental_stream = state_stream[:1000].copy()
        for _ in range(1000) :
            a = incremental_stream[-624]
            b = incremental_stream[-623]
            c = incremental_stream[-227]

            x = ((a & upper) + (b & lower)) & 0xFFFFFFFF
            twisted = c ^ (x >> 1)

            if x & 1 != 0:
                twisted ^= 0x9908b0df
            incremental_stream.append(twisted)
        self.assertEqual(state_stream, incremental_stream)
 
if __name__ == '__main__':
    unittest.main()
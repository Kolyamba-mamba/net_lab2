import unittest
import time
from modelling import modellingSMO


def checkElapsedTime(measuredFunction):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = measuredFunction(*args, **kwargs)
        end = time.time()
        print('[*] elapsed time: {} second'.format(end - start))
        return res
    return wrapper


class MyTestCase(unittest.TestCase):
    # input_stream, count_channels, work_stream, queue_length, count_requests

    @checkElapsedTime
    def test_something(self):
        modellingSMO(0.5, 2, 0.5, 5, 10)
        self.assertEqual(True, True)

    @checkElapsedTime
    def test_something2(self):
        modellingSMO(0.5, 2, 0.5, 5, 30000)
        self.assertEqual(True, True)

    @checkElapsedTime
    def test_something3(self):
        modellingSMO(0.8, 10, 0.2, 20, 50000)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

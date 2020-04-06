# encoding:utf-8
# test for moving average trading indicator

import unittest
import moving_average

REFFERENCED_SMA = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0]

class MovingAverageTest(unittest.TestCase):

    def setUp(self):
        self.ma = moving_average.SimpleMovingAverage('sma', 5, share_name='AAPL')
        self.ma.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def test_get_moving_average_sma(self):
        self.ma.get_moving_average()
        self.assertEqual(self.ma.moving_average, REFFERENCED_SMA)


if __name__ == '__main__':
    unittest.main()

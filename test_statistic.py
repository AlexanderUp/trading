# encoding:utf-8
# tests for statistic module

import unittest

from statistic import StatisticCalc

SOURCE_SEQUENCE = [1, 3, 6, 6, 6, 6, 7, 7, 12, 12, 22]
OTHER_SEQUENCE = [26, 25, 15, 6, 20, 10, 28, 3, 6, 22, 15]

class Test_Statistic(unittest.TestCase):

    def setUp(self):
        self.calc = StatisticCalc(SOURCE_SEQUENCE)

    def test_average(self):
        self.assertEqual(self.calc.average, 8)

    def test_median(self):
        self.assertEqual(self.calc.median, 6)

    # @unittest.expectedFailure
    # @unittest.skip
    def test_mode(self):
        self.assertEqual(self.calc.mode, 6)

    def test_swing(self):
        self.assertEqual(self.calc.swing, 21)

    def test_dispersion(self):
        self.assertAlmostEqual(self.calc.dispersion, 29.090909, 5)

    def test_quality_of_standard_deviation(self):
        self.assertAlmostEqual(self.calc.quality_of_standard_deviation, 5.393599, 5)

    # @unittest.expectedFailure
    def test_covariance(self, other_sequence=OTHER_SEQUENCE):
        other = StatisticCalc(other_sequence)
        self.assertAlmostEqual(self.calc.covariance(other), -10.727273, 5) # -10.727273

    # @unittest.expectedFailure
    def test_correlation(self, other_sequence=OTHER_SEQUENCE):
        other = StatisticCalc(other_sequence)
        self.assertAlmostEqual(self.calc.correlation(other), -0.235586, 5) # -0.235586

if __name__ == '__main__':
    print('*' * 125)
    unittest.main()

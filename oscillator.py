# encoding:utf-8
# oscillators for trading

from moving_frame import MovingFrame
from aux import get_random_bars
from plotter import Plotter


class Oscillator():

    def __init__(self, name, period, data):
        self.indicator_name = name
        self.period = period
        self.data = data
        self.moving_frame = MovingFrame(self.period, self.data)
        self.indicator = None


class RSI(Oscillator):

    VERY_HUGE_NUMBER = 1000000000

    '''
    RSI = 100 — (100 / (1 + RS)),
    RS = U / D, где:
    U — среднее значение положительных ценовых изменений;
    D — среднее значение отрицательных ценовых изменений.
    '''

    def _get_current_frame_rsi(self, frame):
        count_ascending = 0
        value_ascending = 0
        count_descending = 0
        value_descending = 0
        for i in range(len(frame) - 1):
            if frame[i] < frame[i+1]:
                count_ascending += 1
                value_ascending += frame[i+1] - frame[i]
            if frame[i] > frame[i+1]:
                count_descending += 1
                value_descending += frame[i] - frame[i+1]
        try:
            average_ascending = value_ascending / count_ascending
        except ZeroDivisionError as err:
            average_ascending = 0
        try:
            average_descending = value_descending / count_descending
        except ZeroDivisionError as err:
            average_descending = self.VERY_HUGE_NUMBER ** (-1)
        current_frame_rsi = 100 - (100 / (1 + average_ascending / average_descending))
        return current_frame_rsi

    def get_rsi_values(self):
        rsi_values = []
        for frame in self.moving_frame:
            current_frame_rsi = self._get_current_frame_rsi(frame)
            rsi_values.append(current_frame_rsi)
        self.indicator = rsi_values
        return None


class EmaRSI(RSI):

    '''
    RSI = 100 — (100 / (1 + RS)),
    RS = EMA(U) / EMA(D), где:
    EMA - экспоненциальная скользящая средняя;
    U — среднее значение положительных ценовых изменений;
    D — среднее значение отрицательных ценовых изменений.
    '''
    pass


class AwesomeOscillator():
    pass


class Stochastic():
    pass


class MACD():
    pass


class MACDHistogram():
    pass

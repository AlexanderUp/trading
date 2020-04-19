# encoding:utf-8
# oscillators for trading

from moving_frame import MovingFrame
from aux import get_random_bars
from plotter import Plotter


class RSI():
    '''
    RSI = 100 — (100 / (1 + U / D)), где:
    U — среднее значение положительных ценовых изменений;
    D — среднее значение отрицательных ценовых изменений.
    '''
    def __init__(self, name, length, data):
        self.indicator_name = name
        self.length = length
        self.data = data
        self.moving_frame = MovingFrame(self.length, self.data)
        self.indicator = None

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
        average_ascending = value_ascending / count_ascending
        average_descending = value_descending / count_descending
        current_frame_rsi = 100 - (100 / (1 + average_ascending / average_descending))
        return current_frame_rsi


    def get_rsi_values(self):
        rsi_values = []
        for frame in self.moving_frame:
            current_frame_rsi = self._get_current_frame_rsi(frame)
            rsi_values.append(current_frame_rsi)
        self.indicator = rsi_values
        return None


class AwesomeOscillator():
    pass

class Stochastic():
    pass

class MACD():
    pass

class MACDHistogram():
    pass


if __name__ == '__main__':
    print('=' * 125)
    data = get_random_bars(500)
    length = 10
    rsi = RSI('RSI', length, data)
    rsi.get_rsi_values()
    print('{:-^21}'.format('RSI'))
    plotter = Plotter('AAPL', data, rsi)
    plotter.plot()

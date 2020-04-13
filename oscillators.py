# encoding:utf-8
# oscillators for trading

from moving_frame import MovingFrame
from aux import get_random_bars


class RSI():
    '''
    RSI = 100 — (100 / (1 + U / D)), где:
    U — среднее значение положительных ценовых изменений;
    D — среднее значение отрицательных ценовых изменений.
    '''
    def __init__(self, length, data):
        self.length = length
        self.data = data
        self.moving_frame = MovingFrame(self.length, self.data)
        self.rsi_values = None

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
        self.rsi_values = rsi_values
        return None

    def get_rsi_values2(self):
        rsi_valeus = []
        count_ascending = 0
        value_ascending = 0
        count_descending = 0
        value_descending = 0
        for frame in self.moving_frame:
            print('current frame: {}'.format(frame))
            for i in range(len(frame) - 1):
                if frame[i] < frame[i+1]:
                    count_ascending += 1
                    value_ascending += frame[i+1] - frame[i]
                    print('value_ascending: {}'.format(value_ascending))
                if frame[i] > frame[i+1]:
                    count_descending += 1
                    value_descending += frame[i] - frame[i+1]
                    print('value_descending: {}'.format(value_descending))
            average_ascending = value_ascending / count_ascending
            average_descending = value_descending / count_descending
            current_frame_rsi = 100 - (100 / (1 + average_ascending / average_descending))
            rsi_values.append(current_frame_rsi)
            count_ascending = 0
            value_ascending = 0
            count_descending = 0
            value_descending = 0
        self.rsi_values = rsi_values
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
    rsi = RSI(length, data)
    rsi.get_rsi_values2()
    print('{:-^21}'.format('RSI'))

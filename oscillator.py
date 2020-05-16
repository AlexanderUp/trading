# encoding:utf-8
# oscillators for trading

from moving_frame import MovingFrame
from moving_average import SimpleMovingAverage


class Oscillator():

    def __init__(self, data, period):
        self.data = data
        self.period = period
        self.moving_frame = MovingFrame(self.data, self.period)
        self.indicator = None

    def __repr__(self):
        return '{} - period: {} - id: {}'.format(self.indicator_name, self.period, id(self))


class RSI(Oscillator):

    VERY_HUGE_NUMBER = 1000000000

    '''
    RSI = 100 — (100 / (1 + RS)),
    RS = U / D, где:
    U — среднее значение положительных ценовых изменений;
    D — среднее значение отрицательных ценовых изменений.
    '''

    def __init__(self, data, period):
        super().__init__(data, period)
        self.indicator_name = 'RSI'

    def _get_current_frame_value(self, frame):
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

    def get_oscillator_values(self):
        rsi_values = []
        for frame in self.moving_frame:
            _get_current_frame_value = self._get_current_frame_value(frame)
            rsi_values.append(_get_current_frame_value)
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

    def __init__(self, data, period):
        super().__init__(data, period)
        self.indicator_name = 'EMA_RSI'


class Stochastic(Oscillator):

    '''
    Stochastics can be broken down into two lines; %K and %D.

    %K is the percentage of the price at closing (K) within the price range of the number of bars used in the look-back period.
    %K = 100 * (Current Close - Lowest Low) / (Highest High - Lowest Low)

    %D is a smoothed average of %K, to minimize whipsaws while remaining in the larger trend.
    %D = SMA(%K, periodD)

    Lowest Low = The lowest price within the number of recent bars in the look-back period (periodK input)
    Highest High = The highest price within the number of recent bars in the look-back period (periodK input)
    '''

    def __init__(self, data, period_K, period_D):
        super().__init__(data, period=period_K)
        self.indicator_name = 'Stochastic'
        self.period_D = period_D
        self.smoothed_average = None

    def __repr__(self):
        return '{} - period_K: {} - priod_D: {} - id: {}'.format(self.indicator_name, self.period, self.period_D, id(self))


    def get_oscillator_values(self):
        indicator_values = []
        for frame in self.moving_frame:
            lowest_low = min([d.close for d in frame])
            highest_high = max([d.close for d in frame])
            current_close = frame[-1].close
            value = (current_close - lowest_low) / (highest_high - lowest_low) * 100
            indicator_values.append(value)
        self.indicator = indicator_values
        smoothed_average = SimpleMovingAverage(self.indicator, self.period_D)
        smoothed_average.get_moving_average()
        self.smoothed_average = smoothed_average.indicator
        return None

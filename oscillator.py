# encoding:utf-8
# oscillators for trading

from moving_frame import MovingFrame


class Oscillator():

    def __init__(self, data, period):
        self.period = period
        self.data = data
        self.moving_frame = MovingFrame(self.data, self.period)
        self.indicator = None

    def __repr__(self):
        return 'Oscillator - {} - id: {}'.format(self.indicator_name, id(self))


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


class Stochastic():

    '''
    Stochastics can be broken down into two lines; %K and %D.

    %K is the percentage of the price at closing (K) within the price range of the number of bars used in the look-back period.
    %K = SMA(100 * (Current Close - Lowest Low) / (Highest High - Lowest Low), smoothK)
    
    %D is a smoothed average of %K, to minimize whipsaws while remaining in the larger trend.
    %D = SMA(%K, periodD)

    Lowest Low = The lowest price within the number of recent bars in the look-back period (periodK input)
    Highest High = The highest price within the number of recent bars in the look-back period (periodK input)
    '''

    def __init__(self, data, period):
        super().__init__(data, period)
        self.indicator_name = 'Stochastic'

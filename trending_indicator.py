# encoding:utf-8
# trending indicators for trading


from moving_average import SimpleMovingAverage
from moving_average import ExponentialMovingAverage


class AwesomeOscillator():

    '''
    Awesome Oscillator is a trading !!!INDICATOR!!! not oscillator.
    Returned values are not percents.

    lengthAO1 = input(5, minval=1) //5 periods
    lengthAO2 = input(34, minval=1) //34 periods
    AO = sma((high+low)/2, lengthAO1) - sma((high+low)/2, lengthAO2)
    '''

    def __init__(self, data):
        self.indicator_name = 'Awesome Oscillator'
        self.data = data
        self.mid_prices = [0.5 * (d.max + d.min) for d in data]
        self.sma34 = SimpleMovingAverage(self.mid_prices, 34)
        self.sma5 = SimpleMovingAverage(self.mid_prices, 5)
        self.indicator = None

    def __repr__(self):
        return '{} - id: {}'.format(self.indicator_name, id(self))

    def get_oscillator_values(self):
        self.sma34.get_moving_average()
        self.sma5.get_moving_average()
        zipped_values = zip(self.sma5.indicator[-len(self.sma34.indicator):], self.sma34.indicator)
        indicator_values = [(a - b) for (a, b) in zipped_values]
        self.indicator = indicator_values
        return None


class MACD():

    '''
    MACD Line: 12-day EMA - 26-day EMA
    Signal Line: 9-day EMA of MACD Line
    MACD Histogram: MACD Line - Signal Line
    '''

    def __init__(self, data):
        self.indicator_name = 'MACD'
        self.data = [d.close for d in data]
        self.ema12 = ExponentialMovingAverage(self.data, 12)
        self.ema26 = ExponentialMovingAverage(self.data, 26)
        self.macd_line = None
        self.signal_line = None
        self.macd_histogram = None

    def __repr__(self):
        return '{} - id: {}'.format(self.indicator_name, id(self))

    def get_indicator_values(self):
        self.ema12.get_moving_average()
        self.ema26.get_moving_average()
        zipped_values = zip(self.ema12.indicator[-len(self.ema26.indicator):], self.ema26.indicator)
        indicator_values = [(a - b) for (a, b) in zipped_values]
        self.macd_line = indicator_values
        signal_line = ExponentialMovingAverage(self.macd_line, 9)
        signal_line.get_moving_average()
        self.signal_line = signal_line.indicator
        zipped_values_histogram = zip(self.macd_line[-len(self.signal_line):], self.signal_line)
        histogram_values = [(a - b) for (a, b) in zipped_values_histogram]
        self.macd_histogram = histogram_values
        return None

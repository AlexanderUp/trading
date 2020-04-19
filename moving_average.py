# encoding:utf-8
# moving average trading technical indicator

from moving_frame import MovingFrame
from plotter import Plotter
from aux import get_random_bars


class MovingAverage():

    def __init__(self, ma_name, period, data):
        self.indicator_name = ma_name
        self.period = period
        self.data = data
        self.moving_frame = MovingFrame(length=self.period, data=self.data)
        self.indicator = None


class SimpleMovingAverage(MovingAverage):

    def get_moving_average(self):
        moving_average = []
        for frame in self.moving_frame:
            moving_average.append(sum(frame)/len(frame))
        self.indicator = moving_average
        return None


class ExponentialMovingAverage(MovingAverage):

    def get_moving_average(self):
        n = self.period
        r = 2 / (n + 1)
        ema_previous = self.data[0]
        moving_average = [ema_previous]
        for price in self.data[1:]:
            ema = r * price + (1 - r) * ema_previous
            moving_average.append(ema)
            ema_previous = ema
        self.indicator = moving_average
        return None


class SmoothedMovingAverage(MovingAverage):

    def get_moving_average(self):
        n = self.period
        smma_previous = 0
        moving_average = []
        for price in self.data:
            smma = (price + (n - 1) * smma_previous) / n
            moving_average.append(smma)
            smma_previous = smma
        self.indicator = moving_average
        return None


class LinearWeightedMovingAverage(MovingAverage):

    def get_moving_average(self):
        moving_average = []
        numerator = 0
        denominator = 0
        for i, price in enumerate(self.data):
            numerator += (i + 1) * price
            denominator += (i + 1)
            lwma = numerator / denominator
            moving_average.append(lwma)
        self.indicator = moving_average
        return None


if __name__ == '__main__':
    print('*' * 125)
    share_name = 'AAPL'
    data = get_random_bars(500)
    sma = SimpleMovingAverage('sma', 50, data)
    ema = ExponentialMovingAverage('ema', 50, data)
    smma = SmoothedMovingAverage('smma', 50, data)
    lwma = LinearWeightedMovingAverage('lwma', 50, data)
    averages = (sma, ema, smma, lwma)
    for ma in averages:
        ma.get_moving_average()
    plotter = Plotter(share_name, data, *averages)
    plotter.plot()

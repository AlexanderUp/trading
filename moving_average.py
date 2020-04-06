# encoding:utf-8
# moving average trading technical indicator

import matplotlib.pyplot as plt
import random


class MovingAverage():

    def __init__(self, ma_name, period, share_name, data=None):
        self.moving_average_name = ma_name
        self.moving_average_period = period
        self.share_name = share_name
        self.data = data
        self.moving_average = None

    def get_random_bars(self, num_of_frames):
        bars = []
        for i in range(num_of_frames):
            random_bar = random.randint(-5, 5)
            bars = bars + [random_bar]
        self.data = bars
        return None

    def plot(self):
        time_frame = range(len(self.data))
        title = 'Price chart'
        fig = plt.figure(title)
        fig.add_subplot()
        plt.title = title
        plt.grid = True
        plt.xlabel = 'Time'
        plt.ylabel = 'Price'
        plt.plot(time_frame, self.data, label=self.share_name)
        plt.plot(time_frame, self.moving_average, label=self.moving_average_name)
        plt.legend()
        plt.show()


class SimpleMovingAverage(MovingAverage):

    def get_moving_average(self):
        price_pool = []
        moving_average = []
        for price in self.data:
            if len(price_pool) < self.moving_average_period:
                price_pool += [price]
            else:
                price_pool = price_pool[1:] + [price]
            moving_average += [sum(price_pool)/len(price_pool)]
        self.moving_average = moving_average
        return None


class ExponentialMovingAverage(MovingAverage):

    def get_moving_average(self):
        n = len(self.data)
        r = 2 / (n + 1)
        ema_previous = self.data[0]
        moving_average = [ema_previous]
        for price in self.data[1:]:
            ema = r * price + (1 - r) * ema_previous
            moving_average.append(ema)
            ema_previous = ema
        self.moving_average = moving_average
        return None



class SmoothedMovingAverage(MovingAverage):

    def get_moving_average(self):
        n = len(self.data)
        smma_previous = 0
        moving_average = []
        for price in self.data:
            smma = (price + (n - 1) * smma_previous) / n
            moving_average += [smma]
            smma_previous = smma
        self.moving_average = moving_average
        return None


class LinearWeightedAverage(MovingAverage):

    def get_moving_average(self):
        moving_average = []
        price_pool = []
        for price in self.data:
            if len(price_pool) < self.moving_average_period:
                price_pool += [price]
            else:
                price_pool = price_pool[1:] + [price]
            sum_numerator = 0
            sum_divisor = 0
            for i, price_in_pool in enumerate(price_pool):
                sum_numerator += price_in_pool * (i + 1)
                sum_divisor += (i + 1)
            lwma = sum_numerator / sum_divisor
            moving_average += [lwma]
        self.moving_average = moving_average


if __name__ == '__main__':
    print('*' * 125)
    # ma = SimpleMovingAverage('sma', 50, share_name='AAPL')
    # ma = ExponentialMovingAverage('ema', 50, share_name='AAPL')
    # ma = SmoothedMovingAverage('smma', 50, share_name='AAPL')
    ma = LinearWeightedAverage('lwma', 50, share_name='AAPL')
    ma.get_random_bars(500)
    ma.get_moving_average()
    ma.plot()

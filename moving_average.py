# encoding:utf-8
# moving average trading technical indicator

import matplotlib.pyplot as plt
import random
from moving_frame import MovingFrame


class MovingAverage():

    def __init__(self, ma_name, period, share_name, data):
        self.moving_average_name = ma_name
        self.share_name = share_name
        self.data = data
        self.moving_frame = MovingFrame(length=period, data=self.data)
        self.moving_average = None

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
        moving_average = []
        for frame in self.moving_frame:
            moving_average += [sum(frame)/len(frame)]
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


class LinearWeightedMovingAverage(MovingAverage):

    def get_moving_average(self):
        moving_average = []
        # wrong calculation within moving frame ???
        # for frame in self.moving_frame:
        #     numerator = 0
        #     denominator = 0
        #     for i, price in enumerate(frame):
        #         numerator += (i + 1) * price # числитель
        #         denominator += (i + 1) # знаменатель
        #     lwma = numerator / denominator
        numerator = 0
        denominator = 0
        for i, price in enumerate(self.data):
            numerator += (i + 1) * price
            denominator += (i + 1)
            lwma = numerator / denominator
            moving_average += [lwma]
        self.moving_average = moving_average


def get_random_bars(num_of_frames):
    bars = []
    for i in range(num_of_frames):
        random_bar = random.randint(-5, 5)
        bars = bars + [random_bar]
    return bars


if __name__ == '__main__':
    print('*' * 125)
    data = get_random_bars(500)
    # ma = SimpleMovingAverage('sma', 50, 'AAPL', data)
    # ma = ExponentialMovingAverage('ema', 50, 'AAPL', data)
    # ma = SmoothedMovingAverage('smma', 50, 'AAPL', data)
    ma = LinearWeightedMovingAverage('lwma', 50, 'AAPL', data)
    ma.get_moving_average()
    ma.plot()

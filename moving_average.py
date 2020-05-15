# encoding:utf-8
# moving average trading technical indicator


from moving_frame import MovingFrame


class MovingAverage():

    full_indicator_names = {'SMA':'Simple Moving Average',
                            'EMA':'Exponential Moving Average',
                            'SMMA':'Smoothed Moving Average',
                            'LWMA':'LinearWeightedMovingAverage'}

    def __init__(self, data, period):
        self.period = period
        self.data = data
        self.moving_frame = MovingFrame(data=self.data, length=self.period)
        self.indicator = None

    def __repr__(self):
        name = '{}'.format(self.full_indicator_names[self.indicator_name])
        period = 'period = {:<3}'.format(self.period)
        id_ = 'id: {}'.format(id(self))
        return ' - '.join((name, period, id_))


class SimpleMovingAverage(MovingAverage):

    def __init__(self, data, period):
        super().__init__(data, period)
        self.indicator_name = 'SMA'

    def get_moving_average(self):
        moving_average = []
        for frame in self.moving_frame:
            moving_average.append(sum(frame)/len(frame))
        self.indicator = moving_average
        return None


class ExponentialMovingAverage(MovingAverage):

    def __init__(self, data, period):
        super().__init__(data, period)
        self.indicator_name = 'EMA'

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

    def __init__(self, data, period):
        super().__init__(data, period)
        self.indicator_name = 'SMMA'

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

    def __init__(self, data, period):
        super().__init__(data, period)
        self.indicator_name = 'LWMA'

    def get_moving_average(self):
        moving_average = []
        for frame in self.moving_frame:
            numerator = 0
            denominator = 0
            for i, price in enumerate(frame):
                numerator += (i + 1) * price
                denominator += (i + 1)
            lwma = numerator / denominator
            moving_average.append(lwma)
        self.indicator = moving_average
        return None

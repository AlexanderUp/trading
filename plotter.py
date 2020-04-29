# encoding:utf-8
# plotter for trading indicators and oscillators

import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import moving_average
import oscillator
import aux


class Plotter():

    def __init__(self, share_name, data, *args):
        self.share_name = share_name
        self.dates = [d[0] for d in data]
        self.prices = [d[1] for d in data]
        self.functions = [*args]
        print(*self.functions, sep='\n')

    def plot(self):
        title = 'Price chart'
        fig = plt.figure(title)
        fig.add_subplot()
        plt.title = title
        plt.grid = True
        plt.xlabel = 'Time'
        plt.ylabel = 'Price'
        plt.plot_date(mpl.dates.date2num(self.dates), self.prices, linestyle='-', label=self.share_name)
        for f in self.functions:
            plt.plot(self.dates[(len(self.dates) - len(f.indicator)):], f.indicator, label=f.indicator_name + '-{}'.format(str(f.period)))
        # plt.subplots()
        plt.legend()
        plt.show()
        return None


if __name__ == '__main__':
    print('*' * 125)
    share_name = sys.argv[-1].strip('.csv')[-4:]
    data = list(aux.get_historical_data(sys.argv[-1]))
    data.reverse()

    ''' **** Moving Average **** '''
    print('{:-^21}'.format('MOVING AVERAGE'))
    ma_period = 50
    # sma = moving_average.SimpleMovingAverage(ma_period, [price for (date, price) in data])
    # ema = moving_average.ExponentialMovingAverage(ma_period, [price for (date, price) in data])
    # smma = moving_average.SmoothedMovingAverage(ma_period, [price for (date, price) in data])
    # lwma = moving_average.LinearWeightedMovingAverage(ma_period, [price for (date, price) in data])
    # averages = (sma, ema, smma, lwma)
    # averages = (lwma, )
    periods = (10, 50, 100, 200)
    averages = [moving_average.SimpleMovingAverage(period, [price for (date, price) in data]) for period in periods]
    # averages = [moving_average.ExponentialMovingAverage(period, [price for (date, price) in data]) for period in periods]
    # averages = [moving_average.SmoothedMovingAverage(period, [price for (date, price) in data]) for period in periods]
    # averages = [moving_average.LinearWeightedMovingAverage(period, [price for (date, price) in data]) for period in periods]
    for ma in averages:
        ma.get_moving_average()
    plotter = Plotter(share_name, data, *averages)
    plotter.plot()

    ''' **** Oscillator **** '''
    oscillator_period = 10
    print('{:-^21}'.format('RSI'))
    rsi = oscillator.RSI('RSI', oscillator_period, [price for (date, price) in data])
    rsi.get_rsi_values()
    plotter_osc = Plotter(share_name, data, rsi)
    plotter_osc.plot()

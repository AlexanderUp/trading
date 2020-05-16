# encoding:utf-8
# plotter for trading indicators and oscillators

import matplotlib as mpl
import matplotlib.pyplot as plt


class Plotter():

    def __init__(self, share_name, data, *args):
        self.share_name = share_name
        self.dates = [d.date for d in data]
        self.price_close = [d.close for d in data]
        self.price_open = [d.open for d in data]
        self.price_max = [d.max for d in data]
        self.price_min = [d.min for d in data]
        self.functions = [*args]
        print(*self.functions, sep='\n')

    def plot_ma(self):
        title = 'Price chart'
        fig = plt.figure(title)
        plt.title = title
        plt.grid(True)
        plt.xlabel('Time, years')
        plt.ylabel('Price, USD')
        plt.plot_date(mpl.dates.date2num(self.dates), self.price_close, label=self.share_name, linestyle='-', marker=',')
        for f in self.functions:
            plt.plot(self.dates[(len(self.dates) - len(f.indicator)):], f.indicator, label='{}-{}'.format(f.indicator_name, str(f.period)))
        plt.legend()
        plt.show()
        return None

    def plot_osc(self):
        title = 'Price chart'
        fig = plt.figure(title)
        plt.title = title
        for f in self.functions:
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.plot_date(mpl.dates.date2num(self.dates), self.price_close, label=self.share_name, linestyle='-', marker=',')
            ax1.set_ylabel('Price, USD')
            ax1.grid(True)
            ax1.legend()
            ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
            ax2.plot(self.dates[(len(self.dates) - len(f.indicator)):], f.indicator, label='{}-{}'.format(f.indicator_name, str(f.period)), color='r')
            ax2.set_xlabel('Time, years')
            ax2.set_ylabel('%')
            ax2.grid(True)
            ax2.legend()
        plt.show()
        return None

    def plot_trending_ind(self):
        title = 'Price chart'
        fig = plt.figure(title)
        plt.title = title
        for f in self.functions:
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.plot_date(mpl.dates.date2num(self.dates), self.price_close, label=self.share_name, linestyle='-', marker=',')
            ax1.set_ylabel('Price, USD')
            ax1.grid(True)
            ax1.legend()
            ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
            ax2.plot(self.dates[(len(self.dates) - len(f.indicator)):], f.indicator, label='{}'.format(f.indicator_name), color='r')
            ax2.set_xlabel('Time, years')
            ax2.set_ylabel('Delta, USD')
            ax2.grid(True)
            ax2.legend()
        plt.show()
        return None

    def plot_macd(self):
        title = 'Price chart'
        fig = plt.figure(title)
        plt.title = title
        for f in self.functions:
            ax1 = fig.add_subplot(3, 1, 1)
            ax1.plot_date(mpl.dates.date2num(self.dates), self.price_close, label=self.share_name, linestyle='-', marker=',')
            ax1.set_ylabel('Price, USD')
            ax1.grid(True)
            ax1.legend()
            ax2 = fig.add_subplot(3, 1, 2, sharex=ax1)
            ax2.plot(self.dates[(len(self.dates) - len(f.macd_line)):], f.macd_line, label='{}'.format(f.indicator_name), color='r')
            ax2.plot(self.dates[(len(self.dates) - len(f.signal_line)):], f.signal_line, label='MACD Signal Line', color='g')
            ax2.set_xlabel('Time, years')
            ax2.set_ylabel('Delta, USD')
            ax2.grid(True)
            ax2.legend()
            ax3 = fig.add_subplot(3, 1, 3, sharex=ax1)
            ax3.plot(self.dates[(len(self.dates)-len(f.macd_histogram)):], f.macd_histogram, label='MACD Histogram', color='y')
            ax3.set_xlabel('Time, years')
            ax3.set_ylabel('MACD/Signal Line Delta')
            ax3.grid(True)
            ax3.legend()
        plt.show()
        return None

    def plot_stochastic(self):
        title = 'Price chart'
        fig = plt.figure(title)
        plt.title = title
        for f in self.functions:
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.plot_date(mpl.dates.date2num(self.dates), self.price_close, label=self.share_name, linestyle='-', marker=',')
            ax1.set_ylabel('Price, USD')
            ax1.grid(True)
            ax1.legend()
            ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
            ax2.plot(self.dates[(len(self.dates) - len(f.indicator)):], f.indicator, label='{}'.format(f.indicator_name), color='r')
            ax2.plot(self.dates[(len(self.dates) - len(f.smoothed_average)):], f.smoothed_average, label='Stochastic %D', color='g')
            ax2.set_xlabel('Time, years')
            ax2.set_ylabel('%')
            ax2.grid(True)
            ax2.legend()
        plt.show()
        return None

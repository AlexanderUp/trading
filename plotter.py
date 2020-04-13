# encoding:utf-8
# plotter for trading indicators and oscillators

import matplotlib.pyplot as plt


class Plotter():

    def __init__(self, share_name, data, *args):
        self.share_name = share_name
        self.data = data
        self.functions = [*args]
        print(*self.functions, sep='\n')

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
        for f in self.functions:
            plt.plot(time_frame, f.moving_average, label=f.moving_average_name)
        plt.legend()
        plt.show()
        return None

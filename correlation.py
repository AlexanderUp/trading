# encoding:utf-8
# correlation calculator for stocks and futures

import os
import csv
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot

from datetime import datetime

from aux import get_data
from aux import align_data
from statistic import StatisticCalc
from moving_frame import MovingFrame


DATASET_MAIN = 'dataset_main'
DATASET_SECONDARY = 'dataset_secondary'


def calculate_correlation(price_close_outer, price_close_inner):
    statistic_outer = StatisticCalc(price_close_outer)
    statistic_inner = StatisticCalc(price_close_inner)
    correlation = statistic_outer.correlation(statistic_inner)
    return correlation

def calculate_moving_correlation(price_close_outer, price_close_inner, length):
    correlation = []
    moving_frame_a = MovingFrame(price_close_outer, length)
    moving_frame_b = MovingFrame(price_close_inner, length)
    for (a, b) in zip(moving_frame_a, moving_frame_b):
        statistic_a = StatisticCalc(a)
        statistic_b = StatisticCalc(b)
        correlation.append(statistic_a.correlation(statistic_b))
    return correlation

def plot_correlation_chart(data_outer, data_inner, correlation, length):
    name_outer = data_outer[0].name
    name_inner = data_inner[0].name
    title = f'<Correlation {name_outer}/{name_inner}>'
    print(f'Plotting chart {title}...')

    dates = [data_frame.date for data_frame in data_outer]
    price_outer = [data_frame.close for data_frame in data_outer]
    price_inner = [data_frame.close for data_frame in data_inner]

    fig = plt.figure(title)

    host = host_subplot(211)
    par = host.twinx()

    host.set_ylabel(f'Price {name_outer}, USD')
    par.set_ylabel(f'Price {name_inner}, USD')

    p1, = host.plot_date(mpl.dates.date2num(dates), price_outer, label=name_outer, linestyle='-', marker=',', color='r')
    p2, = par.plot_date(mpl.dates.date2num(dates), price_inner, label=name_inner, linestyle='-', marker=',', color='g')
    legend_host = host.legend()

    color_outer = p1.get_color()
    host.yaxis.get_label().set_color(color_outer)
    legend_host.texts[0].set_color(color_outer)

    color_inner = p2.get_color()
    par.yaxis.get_label().set_color(color_inner)
    legend_host.texts[1].set_color(color_inner)

    host.grid(True)
    par.grid(True)

    cor = host_subplot(212, sharex=host)
    cor.set_ylabel('Correlation')
    p3, = cor.plot_date(mpl.dates.date2num(dates[length-1:]), correlation, label=f'<{name_outer}/{name_inner}>', linestyle='-', marker=',', color='b')
    legend_cor = cor.legend()

    color_cor = p3.get_color()
    cor.yaxis.get_label().set_color(color_cor)
    legend_cor.texts[0].set_color(color_cor)
    
    cor.grid(True)

    plt.show()

def calculate_in_loop(target_function, length=100):
    print('****** Correlation calculation ******')

    current_dir = os.getcwd()
    print(f'Current dir: {current_dir}')

    main_dir = os.path.join(current_dir, DATASET_MAIN)
    secondary_dir = os.path.join(current_dir, DATASET_SECONDARY)
    print(f'Main: {main_dir}')
    print(f'Secondary: {secondary_dir}')

    for file_outer in os.listdir(main_dir):
        if file_outer.startswith('.'):
            continue

        print(f'##### File: <{file_outer}> #####')
        path_outer = os.path.abspath(os.path.join(main_dir, file_outer))
        data_outer = get_data(path_outer)

        for file_inner in os.listdir(secondary_dir):
            if file_inner.startswith('.'):
                continue

            path_inner = os.path.abspath(os.path.join(secondary_dir, file_inner))
            data_inner = get_data(path_inner)

            data_outer, data_inner = align_data(data_outer, data_inner)

            price_close_outer = [data_frame.close for data_frame in data_outer]
            price_close_inner = [data_frame.close for data_frame in data_inner]

            correlation = target_function(price_close_outer, price_close_inner)

            if isinstance(correlation, float):
                if abs(correlation) >= 0.7:
                    print('Strong correlation!', end=' ')
                print(f'{os.path.splitext(file_outer)[0]}/{os.path.splitext(file_inner)[0]} >>> {correlation}')
            elif isinstance(correlation, list):
                plot_correlation_chart(data_outer, data_inner, correlation, length)
    print('********** Done! **********')

def main(length=20):
    file_a = sys.argv[-2]
    file_b = sys.argv[-1]
    data_a = get_data(file_a)
    data_b = get_data(file_b)
    data_a, data_b = align_data(data_a, data_b)
    price_close_a = [data_frame.close for data_frame in data_a]
    price_close_b = [data_frame.close for data_frame in data_b]
    correlation = calculate_moving_correlation(price_close_a, price_close_b, length)
    plot_correlation_chart(data_a, data_b, correlation, length)


if __name__ == '__main__':
    print('*'*125)

    # data_a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # data_b = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]
    #
    # mov_a = MovingFrame(data_a, 3)
    # mov_b = MovingFrame(data_b, 3)
    #
    # print(mov_a)
    # print(mov_b)
    #
    # for a in zip(mov_a, mov_b):
    #     print(a)

    # calculate_in_loop(calculate_moving_correlation, 100)
    # calculate_in_loop(calculate_correlation)
    main()

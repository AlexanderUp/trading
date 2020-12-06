# encoding:utf-8
# correlation calculator for stocks and futures


import os
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt

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

def calculate_moving_correlation(price_close_outer, price_close_inner, length=100):
    correlation = []
    moving_frame_a = MovingFrame(price_close_outer, length)
    moving_frame_b = MovingFrame(price_close_inner, length)
    for (a, b) in zip(moving_frame_a, moving_frame_b):
        statistic_a = StatisticCalc(a)
        statistic_b = StatisticCalc(b)
        correlation.append(statistic_a.correlation(statistic_b))
    return correlation

def plot_correlation_chart(data_outer, data_inner, correlation):
    name_outer = data_outer[0].name
    name_inner = data_inner[0].name
    title = f'{name_outer}/{name_inner}'
    print(f'Plotting correlation chart {title}...')
    fig = plt.figure(title)
    plt.title = title
    ax1 = fig.add_subplot(2, 1, 1)
    dates = [data_frame.date for data_frame in data_outer]
    price_outer = [data_frame.close for data_frame in data_outer]
    price_inner = [data_frame.close for data_frame in data_inner]
    ax1.plot_date(mpl.dates.date2num(dates), price_outer, label=name_outer, linestyle='-', marker=',', color='r')
    ax1.set_ylabel(f'Price {name_outer}, USD')
    ax1.grid(True)
    ax1.legend()

    ax2 = ax1.twinx()
    ax2.plot_date(mpl.dates.date2num(dates), price_inner, label=name_inner, linestyle='-', marker=',', color='g')
    ax2.set_ylabel(f'Price {name_inner}, USD')
    ax2.grid(True)
    ax2.legend()

    ax3 = fig.add_subplot(2, 1, 2, sharex=ax1)
    ax3.plot_date(mpl.dates.date2num(dates[99:]), correlation, label=f'Correlation <{name_outer}/{name_inner}>', linestyle='-', marker=',', color='b')
    ax3.set_ylabel('Correlation')
    ax3.grid(True)
    ax3.legend()
    plt.show()

def prepare_data(target_function=calculate_correlation):
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
                # print('Moving frame correlation:')
                # print(correlation)
                plot_correlation_chart(data_outer, data_inner, correlation)
    print('********** Done! **********')


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

    # for a, b in zip(mov_a, mov_b):
    #     print(a)
    #     print(b)
    #     print('*'*50)
    # for a in zip(mov_a, mov_b):
    #     print(a)

    prepare_data(calculate_moving_correlation)

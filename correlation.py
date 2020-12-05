# encoding:utf-8
# correlation calculator for stocks and futures


import os
import csv

from datetime import datetime

from aux import get_data
from aux import align_data
from statistic import StatisticCalc


DATASET_MAIN = 'dataset_main'
DATASET_SECONDARY = 'dataset_secondary'


if __name__ == '__main__':
    print('*'*125)

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

            statistic_outer = StatisticCalc(price_close_outer)
            statistic_inner = StatisticCalc(price_close_inner)

            correlation = statistic_outer.correlation(statistic_inner)
            if abs(correlation) >= 0.7:
                print('Strong correlation!', end=' ')
            print(f'{os.path.splitext(file_outer)[0]}/{os.path.splitext(file_inner)[0]} >>> {correlation}')

    print('********** Done! **********')

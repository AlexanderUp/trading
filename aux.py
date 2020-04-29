# encoding:utf-8
# auxiliary function for trading modules

import random
import csv
import io
from datetime import datetime


def get_random_bars(num_of_frames):
    return [random.randint(-5, 5) for i in range(num_of_frames)]

def to_float(num):
    num = num.replace('.', '')
    num = num.replace(',', '.')
    return float(''.join(num))

def to_date(date):
    day, month, year = date.split('.')
    return datetime(int(year), int(month), int(day))

def get_historical_data(file):
    with open(file, 'r') as f_in:
        reader = csv.reader(f_in)
        next(reader)
        for row in reader:
            # yield to_float(row[1])
            yield (to_date(row[0]), to_float(row[1]))


if __name__ == '__main__':
    import sys
    print('=' * 125)
    file = sys.argv[-1]
    data = list(get_historical_data(file))
    data.reverse()
    print('{:*^30}'.format('DATA'))
    print(*data, sep='\n')

# encoding:utf-8
# auxiliary function for trading modules

import csv

from datetime import datetime
from collections import namedtuple


Data_frame = namedtuple('Data_frame', 'date close open max min')


def price_to_float(price):
    price = ''.join(price.split('.'))
    return float(price.replace(',', '.'))

def get_data(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for item in reader:
            date = item['Date']
            day, month, year = date.split('.')
            date = datetime(int(year), int(month), int(day))
            data.append(Data_frame(date, price_to_float(item['Open']), price_to_float(item['Close']), price_to_float(item['Max']), price_to_float(item['Min'])))
    data.reverse()
    return data

def align_data(data_outer, data_inner):
    '''
    Compare data lenghts and date eqvivalence.
    '''
    res_outer = []
    res_inner = []
    # data_outer = min(len(data_a), len(data_b))
    # data_inner = max(len(data_a), len(data_b))
    for data_point_outer in data_outer:
        for data_point_inner in data_inner:
            if data_point_outer.date == data_point_inner.date:
                res_outer.append(data_point_outer)
                res_inner.append(data_point_inner)
    return res_outer, res_inner

if __name__ == '__main__':
    print('*' * 125)

# encoding:utf-8
# analysis of futures trading


import os
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt


import statistic


from collections import namedtuple
from datetime import datetime


Futures = namedtuple('futures', 'date open high low close')


FUTURES_RTS = os.path.expanduser('~/Downloads/RTS.csv')
FUTURES_GOLD = os.path.expanduser('~/Downloads/GOLD.csv')
FUTURES_MIX = os.path.expanduser('~/Downloads/MIX.csv')


def convert_price(price):
    price = ''.join(price.split('.'))
    return float(price.replace(',', '.'))

def get_data(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for item in reader:
            date = item['Date']
            year, month, day = reversed(date.split('.'))
            date = datetime(int(year), int(month), int(day))
            data.append(Futures(date, convert_price(item['Open']), convert_price(item['Close']), convert_price(item['Max']), convert_price(item['Min'])))
    return data

def plot_future_data(future_name, data, depo, currency):
    title = f'Future <{future_name}>'
    fig = plt.figure(title)
    plt.title = title

    dates = [mpl.dates.date2num(future.date) for future in data]
    prices = [future.close for future in data]
    depo_data = [data[0] for data in depo]

    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot_date(dates, prices, label=title, linestyle='-', marker=',' )
    ax1.set_ylabel(f'Price, {currency}')
    ax1.grid(True)
    ax1.legend()

    ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
    ax2.plot_date(dates, depo_data, label='Depo', linestyle='-', marker=',')
    ax2.set_xlabel('Date')
    ax2.set_ylabel(f'Price, {currency}')
    ax2.grid(True)
    ax2.legend()

    plt.show()

def get_total_depo(data, depo, point_price):
    data.sort()
    previous_day_future = data[0]
    yield (depo, 0)
    for future in data[1:]:
        margin_diff = future.close - previous_day_future.close
        previous_day_future = future
        price_change = margin_diff * point_price
        depo += price_change
        print(f'Diff: {price_change:>15.6f}; depo: {depo:>15.6f}', future)
        yield (depo, price_change)


if __name__ == '__main__':
    print('*' * 125)

    # file = FUTURES_GOLD
    # initial_depo = 500
    # point_price = 1
    # currency = 'USD'

    # file = FUTURES_RTS
    # initial_depo = 40000
    # point_price = 1.5
    # currency = 'RUR'

    # file = FUTURES_MIX
    # initial_depo = 40000
    # point_price = 1
    # currency = 'RUR'

    # future_name = os.path.basename(file).split('.')[0]
    # data = get_data(file)
    # depo = list(get_total_depo(data, initial_depo, point_price))
    # plot_future_data(future_name, data, depo, currency)

    data_rts = [future.close for future in get_data(FUTURES_RTS)]
    statistic_rts = statistic.StatisticCalc(data_rts)

    data_gold = [future.close for future in get_data(FUTURES_GOLD)]
    statistic_gold = statistic.StatisticCalc(data_gold)

    data_mix = [future.close for future in get_data(FUTURES_MIX)]
    statistic_mix = statistic.StatisticCalc(data_mix)

    print('***** Correlation *****')

    print(f'RTS-GOLD: \t{statistic_rts.correlation(statistic_gold):<15}')
    print(f'GOLD-RTS: \t{statistic_gold.correlation(statistic_rts):<15}')

    print(f'RTS-MIX: \t{statistic_rts.correlation(statistic_mix):<15}')
    print(f'MIX-RTS: \t{statistic_mix.correlation(statistic_rts):<15}')

    print(f'MIX-GOLD: \t{statistic_mix.correlation(statistic_gold):<15}')
    print(f'GOLD-MIX: \t{statistic_gold.correlation(statistic_mix):<15}')

# encoding:utf-8
# test for plotter module

# pip3 install mpl-finance
# from mpl_finance import candlestick_ohlc

import sys
import moving_average
import oscillator
import trending_indicator
import aux

from plotter import Plotter


print('*' * 125)
share_name = sys.argv[-1].strip('.csv')[-4:]
data = list(aux.get_historical_data(sys.argv[-1]))
data.reverse()

# ''' **** Moving Average **** '''
print('{:-^21}'.format('MOVING AVERAGE'))
ma_period = 50
sma = moving_average.SimpleMovingAverage([price.close for price in data], ma_period)
ema = moving_average.ExponentialMovingAverage([price.close for price in data], ma_period)
smma = moving_average.SmoothedMovingAverage([price.close for price in data], ma_period)
lwma = moving_average.LinearWeightedMovingAverage([price.close for price in data], ma_period)
averages = (sma, ema, smma, lwma)
# averages = (lwma, )
# periods = (10, 50, 100, 200)
# averages = [moving_average.SimpleMovingAverage([price.close for price in data], period) for period in periods]
# averages = [moving_average.ExponentialMovingAverage([price.close for price in data], period) for period in periods]
# averages = [moving_average.SmoothedMovingAverage([price.close for price in data], period) for period in periods]
# averages = [moving_average.LinearWeightedMovingAverage([price.close for price in data], period) for period in periods]
for ma in averages:
    ma.get_moving_average()
plotter = Plotter(share_name, data, *averages)
plotter.plot_ma()

''' **** Oscillators **** '''
oscillator_period = 10
print('{:-^21}'.format('RSI'))
rsi = oscillator.RSI([price.close for price in data], oscillator_period)
rsi.get_oscillator_values()
plotter_osc = Plotter(share_name, data, rsi)
plotter_osc.plot_osc()

''' **** Trending Indicators **** '''
print('{:-^21}'.format('AwesomeOscillator'))
aosc = trending_indicator.AwesomeOscillator(data)
aosc.get_oscillator_values()
plotter_osc = Plotter(share_name, data, aosc)
plotter_osc.plot_trending_ind()

''' **** MACD ****'''
print('{:-^21}'.format('MACD'))
macd = trending_indicator.MACD(data)
macd.get_indicator_values()
plotter_macd = Plotter(share_name, data, macd)
plotter_macd.plot_macd()

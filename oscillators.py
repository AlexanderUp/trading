# encoding:utf-8
# oscillators for trading

from moving_frame import MovingFrame

class RSI():
    '''
    RSI = 100 — (100 / (1 + U / D)), где:
    U — среднее значение положительных ценовых изменений;
    D — среднее значение отрицательных ценовых изменений.
    '''
    def __init__(self, length, data):
        self.moving_frame = MovingFrame(length, data)


if __name__ == '__main__':
    print('=' * 125)
    

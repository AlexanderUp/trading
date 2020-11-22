# encoding:utf-8
# moving frame for trading related calculations


import collections


class MovingFrame():

    def __init__(self, data, length):
        '''
        Priming initial frame by sequence of first n values of the data.
        '''
        self.data = data
        self.length = length
        self.deq = collections.deque(maxlen=self.length)

    def __iter__(self):
        for value in self.data:
            self.deq.append(value)
            if len(self.deq) == self.length:
                yield self.deq


if __name__ == '__main__':
    print('=' * 125)

    import time

    numbers = 25000000
    length = 1000
    data = [i for i in range(numbers)]

    print('---- doing {} times, length {} ----'.format(numbers, length))

    print('---- deque ----')
    moving_frame = MovingFrame(data, length)
    time_start = time.time()
    count = 0
    for frame in moving_frame:
        sum(frame)
    time_end = time.time()
    print('---- Elapsed time: {} seconds ----'.format(time_end - time_start))

    print('---- list ----')
    i_list = [0] * length
    time_start = time.time()
    for i in data:
        i_list = i_list[1:] + [i]
        sum(i_list)
    time_end = time.time()
    print('---- Elapsed time: {} seconds ----'.format(time_end - time_start))

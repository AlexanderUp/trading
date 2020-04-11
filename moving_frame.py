# encoding:utf-8
# moving frame for trading related calculations

import collections


class MovingFrame():

    def __init__(self, length, data):
        self.deq = collections.deque(maxlen=length)
        self.data = data

    def __iter__(self):
        for item in self.data:
            self.deq.append(item)
            yield self.deq


if __name__ == '__main__':
    import time
    print('=' * 125)
    numbers = 25000000
    length = 1000
    data = [i for i in range(numbers)]
    print('---- doing {} times, length {} ----'.format(numbers, length))
    moving_frame = MovingFrame(length, data)
    time_start = time.time()
    count = 0
    for frame in moving_frame:
        sum(frame)
        continue
    time_end = time.time()
    print('---- deque ----')
    print('---- Elapsed time: {} seconds ----'.format(time_end - time_start))
    i_list = [0] * length
    time_start = time.time()
    for i in data:
        i_list = i_list[1:] + [i]
        sum(i_list)
    time_end = time.time()
    print('---- list ----')
    print('---- Elapsed time: {} seconds ----'.format(time_end - time_start))
    print('-' * 125)

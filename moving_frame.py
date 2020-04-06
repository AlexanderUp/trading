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
    # data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    data = [i for i in range(10000000)]
    time_start = time.time()
    moving_frame = MovingFrame(4, data)
    for frame in moving_frame:
        # print('{} => sum: {}, length: {}'.format(frame, sum(frame), len(frame)))
        continue
    print('---- Elapsed time: {} seconds ----'.format(time.time()-time_start))
    print('-' * 125)

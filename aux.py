# encoding:utf-8
# auxiliary function for trading modules

import random


def get_random_bars(num_of_frames):
    bars = []
    for i in range(num_of_frames):
        random_bar = random.randint(-5, 5)
        bars = bars + [random_bar]
    return bars

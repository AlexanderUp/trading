# encoding:utf-8
# auxiliary function for trading modules

import random


def get_random_bars(num_of_frames):
    return [random.randint(-5, 5) for i in range(num_of_frames)]

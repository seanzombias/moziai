#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : buffer.py
# Create date : 2019-10-20 19:33
# Modified date : 2019-10-20 21:46
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

import numpy as np
import random
from collections import deque

class MemoryBuffer:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)
        self.maxSize = size
        self.len = 0

    def sample(self, count):
        batch = []
        count = min(count, self.len)
        batch = random.sample(self.buffer, count)

        s_arr = np.float32([arr[0] for arr in batch])
        a_arr = np.float32([arr[1] for arr in batch])
        r_arr = np.float32([arr[2] for arr in batch])
        s1_arr = np.float32([arr[3] for arr in batch])

        return s_arr, a_arr, r_arr, s1_arr

    def len(self):
        return self.len

    def add(self, s, a, r, s1):
        trainsition = (s,a,r,s1)
        self.len += 1
        if self.len > self.maxSize:
            self.len = self.maxSize
        self.buffer.append(trainsition)

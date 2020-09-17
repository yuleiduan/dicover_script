# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
from random import random
import math


def stochastic(lower, upper):
    return int(math.floor(random() * (upper - lower) + lower))


#
# str = 5
# nub = 3890
# print(math.floor(nub*0.7))
# for i in range(str-1):
#     print(stochastic(math.floor(nub*0.05), math.floor(nub*0.7)))


def lvarr(a, list):
    b = []
    pv_list = []
    for i in range(list):
        b.append(round(random() * (10 - 1) + 1, 2))
    d = 0
    c = 0
    for i in b:
        c += i
    for j in b:
        d += j / c
        pv_list.append(math.floor(a * (j / c)))
    return pv_list
# print(lvarr(3000, 2))

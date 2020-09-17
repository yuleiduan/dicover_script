# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# 中位数
def huahua(x):
    length = len(x)
    print(length)
    x.sort()
    print(x)
    if (length % 2) == 1:
        z = length // 2
        y = x[z]
    else:
        y = (x[length // 2] + x[length // 2 - 1]) / 2
    return y
b = [4215, 4713, 2, 1, 4545, 4399, 4050, 1, 4646, 4154, 4897, 2752, 3240, 2500, 2806, 2288, 3587, 3023, 2945, 2913, 4495, 4120, 5015, 4217, 3275, 2150, 3386, 3003, 2331, 3168, 4564, 4433, 6462, 5318, 5718, 6007, 5609, 6233, 5311, 5522]

print(huahua(b))

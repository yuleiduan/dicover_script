# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import math
import random
import time
from datetime import datetime
import datetime as b
from jieba import xrange


class timeclass:
    def __init__(self):
        self.start = self.current()[1]
        self.end = self.timeTomorrow()

    def strTimeProp(self, prop, frmt):
        stime = time.mktime(time.strptime(self.start, frmt))
        etime = time.mktime(time.strptime(self.end, frmt))
        ptime = stime + prop * (etime - stime)
        return int(ptime)

    # 时间戳随机时间
    def randomTimestamp(self, frmt='%Y-%m-%d %H:%M:%S'):
        return self.strTimeProp(random.random(), frmt)

    # 随机时间
    def randomDate(self, frmt='%Y-%m-%d %H:%M:%S'):
        return time.strftime(frmt, time.localtime(self.strTimeProp(random.random(), frmt)))

    # 调用生成随机时间批量生成秒
    def randomTimestampList(self, n, frmt='%Y-%m-%d %H:%M:%S'):
        return [self.randomTimestamp(frmt) for _ in xrange(n)]

    # 调用生成随机时间函数批量生成时间
    def randomDateList(self, n, frmt='%Y-%m-%d %H:%M:%S'):
        return [self.randomDate(frmt) for _ in xrange(n)]

    # 随机时间减当前时间转成秒
    def latency_time(self):
        return int(self.itemMsec(self.randomDate()) - self.itemMsec(self.start)) + self.number(18030)

    # 当前时间
    def current(self):
        sky = time.strftime("%Y-%m-%d", time.localtime())
        second = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return [sky, second]

    # 时间戳秒
    def itemMsec(self, timestr):
        datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        obj_stamp = int(time.mktime(datetime_obj.timetuple()) + datetime_obj.microsecond / 1000.0)
        return obj_stamp

    # 转换成时间格式
    def timeStamp(self, timenum):
        stamp = float(timenum / 1000)
        timeArray = time.localtime(stamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    # 明天时间
    def timeTomorrow(self):
        today = b.date.today()
        tomorrow = today + b.timedelta(days=1)
        tomorrow_start_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
        a = str(tomorrow_start_time) + "000"
        d = self.timeStamp(int(a))
        return d

    def number(self, x):
        if isinstance(x, int):
            price = random.randint(0, x)
        elif isinstance(x, list):
            num = random.randint(0, len(x) - 1)
            price = x[num]
        elif isinstance(x, dict):
            num = random.randint(0, len(x) - 1)
            price = x[num]
        else:
            print('输入类型或长度错误')
            price = "error: 输入类型或长度错误"
        return price


# if __name__ == "__main__":
#     variable = timeclass()
#     print(str(variable.latency_time()))
#     # 随机时间
#     random_time = variable.randomDate()
#     print(random_time)
#     print(variable.itemMsec(random_time))
#     print(variable.start)
#     print(math.floor(round((variable.itemMsec(variable.start)-variable.itemMsec("2020-07-31 00:39:16"))/3600/24, 0)))
#     # 时间戳毫秒  可以用来做等待时间
#     current_ss = variable.itemMsec(random_time) - variable.itemMsec(variable.start)
#     print(current_ss)
#     variable.latency_time()

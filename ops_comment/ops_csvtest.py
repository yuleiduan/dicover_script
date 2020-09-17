# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import requests
import re
import copy
import json
from time import sleep

from pip._vendor.retrying import retry


class threadgroup_2:
    def __init__(self, t_id, t_user, text, sleep_s):
        self.id = t_id
        self.text = text
        self.t_sleep = sleep_s
        self.user = t_user
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.109 Safari/537.36'}
        self.url = "http://www.pandabox.top"

    @retry(stop_max_attempt_number=3)
    def git_Cookie(self):
        request = requests.get(self.url + "/luka/api/user/login", headers=self.header,
                               params={"uid": self.user, "pswd": "1qa@WS3ed4rf==!!"})
        print("git_Cookie: " + str(request.status_code) + "  id" + str(self.id))
        head = request.headers
        self.header["luka-session"] = head["luka-session"]
        self.header["Set-Cookie"] = head["Set-Cookie"]
        self.header["content-type"] = head["Content-Type"]
        return self.header

    @retry(stop_max_attempt_number=5)
    def discover_commnt(self):
        data_json = json.dumps({"rid": self.id, "ct": self.text})
        # print(data_json)
        ss = requests.post(self.url + '/luka/api/water/comment/save_water_comment', headers=self.header,
                           data=data_json)
        # print(ss.text)
        # print(ss.headers)
        print(self.t_sleep)
        sleep(self.t_sleep)



def a():
    data = csv.reader(open('../Comment_csv/评论次数7.csv', encoding='utf-8'), delimiter=',')
    sortedlist = sorted(data, key=lambda x: int(x[3]))
    return sortedlist


if __name__ == "__main__":
    b = a()
    for i in range(len(b)):
        if int(i - 1) > 0:
            a = threadgroup_2(b[i][0], b[i][1], b[i][2], int(b[i][3]) - int(b[i - 1][3]))
            a.git_Cookie()
            a.discover_commnt()
        else:
            a = threadgroup_2(b[i][0], b[i][1], b[i][2], int(b[i][3]))
            a.git_Cookie()
            a.discover_commnt()
        sleep(0.2)

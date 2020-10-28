# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import re
import copy
from time import sleep

from pip._vendor.retrying import retry
import math
from data.time_class import *
from random import random


# 随机
def stochastic(lower, upper):
    return int(math.floor(random() * (upper - lower) + lower))


class PV:
    def __init__(self):
        self.item = {}
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.109 Safari/537.36'}
        self.url = "http://www.pandabox.top"
        # self.test_url = "http://test.pandacase.cn"
        # self.test_uid = 1258571561642934272
        # self.test_password = "k4B5Xy"
        self.uid = 1161294774320484352
        self.password = "WIQpPi"

    def stochastic(self, lower, upper):
        return int(math.floor(random() * (upper - lower) + lower))

    @retry(stop_max_attempt_number=3)
    def git_Cookie(self):
        # 获取Cookie
        request = requests.get(self.url + "/luka/api/user/login", headers=self.header,
                               params={"uid": self.uid, "pswd": self.password})
        if request.status_code != 200:
            print(request.text)
            print('git_Cookie:' + "请求失败")
            return
        b = request.headers
        self.header["luka-session"] = b["luka-session"]
        self.header["Set-Cookie"] = b["Set-Cookie"]
        sleep(0.3)
        return copy.deepcopy(self.header)

    # 使用大咖id获取所有发现id
    @retry(stop_max_attempt_number=3)
    def discover_id(self, kol_id):
        ids = []
        for id in kol_id:
            try:
                sleep(1)
                request = requests.get(self.url + "/luka/api/user/kol/discover_list", headers=self.header,
                                       params={"kolId": id, "pageNo": 0, "limit": 100})
                if request.status_code != 200:
                    print("discover_page失败", request.text)
                    continue
                a = request.json()['dt']
                sd = []
                for i in range(len(a)):
                    ids.append(a[i]["id"])
                    sd.append(a[i]["id"])
                print(sd)
            except Exception as e:
                print(e)
        print(ids)
        return ids

    # 获取全部列表的大咖id
    @retry(stop_max_attempt_number=3)
    def kol_list(self):
        sleep(0.3)
        request = requests.get(self.url + "/luka/api/user/kolIdAndNamesByType", headers=self.header,
                               params={"typeId": 0})
        if request.status_code != 200:
            print("出错")
            return
        r = request.json()["dt"]
        print(len(r))
        c = []
        for i in range(len(r)):
            c.append(r[i]["uid"])
        c.append('7003946')
        return c

    def discover_page(self, discover_id):
        try:
            request = requests.get(self.url + "/luka/api/user/kol/discover_detail", headers=self.header,
                                   params={"discoverId": discover_id, "on_shelf": "true"})
            if request.status_code != 200:
                print('discover_page:' + "----------请求失败ID:", discover_id)
                if request.json()["em"] == "微信授权URL":
                    PV.git_Cookie(self)
                return
            sleep(0.3)
        except Exception as e:
            print(e)
            sleep(2)

    @retry(stop_max_attempt_number=3)
    def discover_pages(self, c_id):
        request = requests.get(self.url + "/luka/api/user/kol/discover_detail", headers=self.header,
                               params={"discoverId": c_id, "on_shelf": "true"})
        if request.status_code != 200:
            print('discover_page:' + "----------请求失败ID:", c_id)
            return
        em = request.json()
        self.item["ss"] = em["ss"]
        if em["ss"] == False:
            return self.item
        self.item["vc"] = em['dt']['vc']
        self.item["pt"] = em['dt']['pt']
        run = timeclass()
        sky = math.floor(round((run.itemMsec(run.start) - run.itemMsec(self.item["pt"])) / 3600 / 24, 0))
        self.a(c_id, sky, self.item["vc"])
        return self.item

    def browsetype_1(self, id_list, s):
        if s > 300:
            return
        ci = stochastic(100, 500)
        print(ci)
        print("第一天刷取%s次，id%s" % (ci, id_list))
        for l in range(ci):
            try:
                self.discover_page(id_list)
            except:
                self.discover_page(id_list)
            continue

    def browsetype_2(self, id_list, s):
        x = 0
        if s < 200:
            x = 200 - s
        ci = stochastic(100, 600) + x
        print("第二天刷取%s次，id%s" % (ci, id_list))
        for l in range(ci):
            try:
                self.discover_page(id_list)
            except:
                self.discover_page(id_list)
            continue

    def browsetype_3(self, id_list, s):
        x = 0
        if s < 400:
            x = 400 - s
        ci = stochastic(100, 400) + x
        print("第三天刷取%s次，id%s" % (ci, id_list))
        for l in range(ci):
            try:
                self.discover_page(id_list)
            except:
                self.discover_page(id_list)
            continue

    def browsetype_4(self, id_list):
        ci = stochastic(10, 120)
        print("超过三天刷取%s次，id%s" % (ci, id_list))
        for l in range(ci):
            try:
                self.discover_page(id_list)
            except:
                self.discover_page(id_list)
            continue

    def a(self, d_type, sky, vc):
        if sky == 0 or vc < 200:
            self.browsetype_1(d_type, vc)
        elif sky == 1 or vc < 400:
            self.browsetype_2(d_type, vc)
        elif sky == 2 or vc < 600:
            self.browsetype_3(d_type, vc)
        elif sky > 2:
            self.browsetype_4(d_type)
        else:
            print("--文章未到发布日期")


if __name__ == '__main__':
    run = PV()
    run.git_Cookie()
    kol_id_list = run.kol_list()
    discover_id_list = run.discover_id(kol_id_list)
    for i in range(len(discover_id_list)):
        run.discover_pages(discover_id_list[i])
    # a = run.stochastic(1900, 2400)
    # print(a)
    # for i in range(a):
    #     run.discover_page(291)

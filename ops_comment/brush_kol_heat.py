# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import math

import requests
import copy
from time import sleep

from pip._vendor.retrying import retry
from data.time_class import *
from random import random
import math


def stochastic(lower, upper):
    """两数之间随机数"""
    return int(math.floor(random() * (upper - lower) + lower))


class PV:
    def __init__(self):
        self.item = {}
        self.url = "http://www.pandabox.top"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.109 Safari/537.36'}

    @retry(stop_max_attempt_number=3)
    def git_Cookie(self):
        """获取Cookie"""
        request = requests.get(self.url + "/luka/api/user/login", headers=self.header, params={"uid": 1161294774320484352, "pswd": "WIQpPi"})
        if request.status_code != 200:
            print('git_Cookie:' + "请求失败", request.text)
            return
        response = request.headers
        self.header["luka-session"] = response["luka-session"]
        self.header["Set-Cookie"] = response["Set-Cookie"]
        return copy.deepcopy(self.header)

    @retry(stop_max_attempt_number=3)
    def kol_list(self):
        """获取全部列表的大咖id
        :return: list：所有大咖id加上了官方大咖"""
        sleep(0.3)
        request = requests.get(self.url + "/luka/api/user/kolIdAndNamesByType", headers=self.header, params={"typeId": 0})
        if request.status_code != 200:
            print("出错")
            return
        response = request.json()["dt"]
        print("所有大咖人数%s" % len(response))
        kol_id_list = ['7003946']
        for kol_element in range(len(response)):
            kol_id_list.append(response[kol_element]["uid"])
        return kol_id_list

    @retry(stop_max_attempt_number=3)
    def discover_id(self, kol_id):
        """使用大咖id获取所有发现id
        :param kol_id: 大咖id
        :return: 返回大咖名下的所有发现文章id
        """
        cid_list = []
        for id in kol_id:
            try:
                sleep(1)
                request = requests.get(self.url + "/luka/api/user/kol/discover_list", headers=self.header,
                                       params={"kolId": id, "pageNo": 0, "limit": 100})
                if request.status_code != 200:
                    print("discover_page失败", request.text)
                    continue
                response = request.json()['dt']
                for dt in range(len(response)):
                    cid_list.append(response[dt]["id"])
            except Exception as e:
                print(e)
        print("文章数量%s\n文章列表%s" % (len(cid_list),cid_list))
        return cid_list

    @retry(stop_max_attempt_number=3)
    def discover_page(self, discover_id):
        """发现页面,获取页面的评论数浏览量以及发布时间"""
        request = requests.get(self.url + "/luka/api/user/kol/discover_detail", headers=self.header,
                               params={"discoverId": discover_id, "on_shelf": "true"})
        if request.status_code != 200:
            print('discover_page:' + "请求失败ID:", discover_id)
            if request.json()["em"] == "微信授权URL":
                self.git_Cookie()
        else:
            sleep(0.3)
            return request

    @retry(stop_max_attempt_number=3)
    def page_data(self, c_id) -> dict:
        """
        :param c_id: 发现文章 id
        :return: 文章的vc：浏览数 pt：发布日期"""
        response = self.discover_page(c_id).json()
        if not response["ss"]:
            return self.item
        else:
            self.item["vc"] = response['dt']['vc']
            self.item["pt"] = response['dt']['pt']
            # 获取已发布文章天数
            times = timeclass()
            sky = math.floor(round((times.itemMsec(times.start) - times.itemMsec(self.item["pt"])) / 3600 / 24, 0))
            if sky >= 100:
                if self.item["vc"] < 2500:
                    Random_number = stochastic(5, 120)
                    self.brush_number(Random_number, c_id)
                else:
                    print("文章%s天数发布日期已%s天，浏览量%s" % (c_id, sky, self.item["vc"]))
            else:
                self.run(c_id, sky, self.item["vc"])
            return self.item

    def brush_number(self, Random_number, cid):
        for i in range(Random_number):
            try:
                self.discover_page(cid)
            except Exception as e:
                print("请求错误%s" % e)
                self.discover_page(cid)
            continue

    def run(self, cid, sky, vc):
        """
        :param cid: 发现文章id
        :param sky: 文章已发布天数
        :param vc: 发现浏览量
        :return: None"""
        if sky == 0 or vc < 200:
            if vc > 300:
                print("%s数量达标" % cid)
            else:
                Random_number = stochastic(100, 500)
                print("第一指标刷取%s次，id%s" % (Random_number, cid))
                self.brush_number(Random_number, cid)
        elif sky == 1 or vc < 400:
            Random_number = stochastic(100, 600) + 200 - (vc if vc < 200 else 0)
            print("第二指标%s次，id%s" % (Random_number, cid))
            self.brush_number(Random_number, cid)
        elif sky == 2 or vc < 600:
            Random_number = stochastic(100, 600) + 200 - (vc if vc < 400 else 0)
            print("第三指标刷取%s次，id%s" % (Random_number, cid))
            self.brush_number(Random_number, cid)
        elif sky > 2:
            Random_number = stochastic(5, 120)
            print("超过三天刷取%s次，id%s" % (Random_number, cid))
            self.brush_number(Random_number, cid)
        else:
            print("文章未到发布日期")


if __name__ == '__main__':
    run = PV()
    run.git_Cookie()
    kol_ids = run.kol_list()
    discover_id_list = run.discover_id(kol_ids)
    for i in range(len(discover_id_list)):
        run.page_data(discover_id_list[i])

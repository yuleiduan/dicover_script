# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import time
from pip._vendor.retrying import retry

import requests
import copy
from data.time_class import *
import csv
from data.comment_test import *
import math


class Threadgroup_1(timeclass):
    def __init__(self, t_id=None, t_user_number=None, file=None):
        timeclass.__init__(self)
        self.id = t_id
        self.file = file
        self.user_number = t_user_number
        self.item = {}
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.109 Safari/537.36'}
        self.url = "http://www.pandabox.top"

    def git_Cookie(self):
        # 获取Cookie
        request = requests.get(self.url + "/luka/api/user/login", headers=self.header,
                               params={"uid": 1161294774320484352, "pswd": "WIQpPi"})
        if request.status_code != 200:
            print('git_Cookie:' + "请求失败")
            return
        b = request.headers
        self.header["luka-session"] = b["luka-session"]
        self.header["Set-Cookie"] = b["Set-Cookie"]
        time.sleep(0.2)
        return copy.deepcopy(self.header)

    def discover_page(self, cc, shuijunIDlist):
        # 返回需要评论条数
        request = requests.get(self.url + "/luka/api/user/kol/discover_detail", headers=self.header,
                               params={"discoverId": self.id, "on_shelf": "true"})
        if request.status_code != 200:
            print('discover_page:' + "----------请求失败ID:", self.id)
            return
        if request.json()["ss"] == "false":
            print("大咖发现不存在")
            return
        elment = request.json()["dt"]
        self.item["id"] = self.id
        self.item["vc"] = elment["vc"]
        self.item["cc"] = elment["cc"]
        self.item["discover_type"] = elment["t"]
        self.item["kolUser"] = elment["userId"]
        element_text = elment["chtml"]
        s = re.sub(r'<.+?>|“|”|&(.+?);', "", element_text)
        a = re.sub(r'|\s|]t|\ufeff|\u3000', "", s)
        pattern = re.compile(r'\\t|\t')
        a = re.sub(pattern, ' ', a)
        c = re.sub(r'。|\.|,|;|；|!|！', "，", a)
        g = c.split("，")
        for i in g:
            if len(i) < 10 or len(i) > 100:
                g.remove(i)
        if len(g) > 30:
            self.item["discover_text"] = g
        else:
            self.item["discover_text"] = []
        # ------------------
        vc_1 = int(self.item["vc"]) / 1000
        item = {'0': 10, '1': 5, '2': 9, '3': 8, '4': 6, '5': 3, '6': 1, '7': 2, '8': 4, '9': 7}

        def nunber(id):
            if item[id]:
                a = item[id]
                return a

        nu = ''
        for j in str(self.id):
            nu = nu + str(nunber(j))
        vc_1 = vc_1 * (int(nu) % 12 + 4)

        # -------------------

        if int(vc_1) > int(self.item["cc"]) and int(self.item["vc"]) < 20000:
            cc_add = math.ceil((int(vc_1) - int(self.item["cc"])) / 2)  # 控制数量
            b = int(int(self.item["vc"]) / 100)  # 得道百位数及以上
            q = int(int(self.item["vc"]) % 100 / 10)  # 十位
            s = int(int(self.item["vc"]) % 1000 % 10)  # 个位
            bs = number(9)
            if (b + q + bs) % 2 == 0:
                li = 0
                for y in range(int(cc_add)):
                    if number(9) == s:
                        li += number(2)
                self.item["commentID_number"] = li + int(cc_add)
            else:
                self.item["commentID_number"] = int(cc_add)
        else:
            self.item["commentID_number"] = 0
        time.sleep(0.5)
        self.kol_user(cc, shuijunIDlist)
        return self.header

    def kol_user(self, cc, shuijunIDlist):
        # 用大咖id获取大咖的名字
        request = requests.get(self.url + '/luka/api/user/kol_detail?kolId=' + self.item["kolUser"],
                               headers=self.header)
        if request.status_code != 200:
            print('kol_user:' + "请求失败")
            print(request.text)
            return
        elment = request.json()["dt"]
        self.item["kol_name"] = elment["dn"]
        time.sleep(0.2)
        self.kol_tpye(cc, shuijunIDlist)
        return self.header

    def kol_typelist(self):
        # 获取所有type分类的内容
        request = requests.get(self.url + "/luka/api/user/kol_type", headers=self.header)
        type = request.json()["dt"]
        kol_type = {}
        for i in range(1, len(type)):
            request = requests.get(self.url + '/luka/api/user/kolIdAndNamesByType', headers=self.header,
                                   params={"typeId": i})
            time.sleep(1)
            kol_type[i] = request.text
        return kol_type

    def kol_tpye(self, cc, shuijunIDlist):
        for s in range(math.floor(self.item["commentID_number"])):
            # 获取大咖在那个type下
            kol_list_type = []
            for i in range(1, len(cc)):
                dd = re.findall(self.item["kol_name"], cc[i])
                if dd:
                    kol_list_type.append(i)
            self.item["kol_tpye_id"] = kol_list_type
            self.discover_csv(shuijunIDlist)
        return self.header

    def discover_pv(self):
        # 发现加1浏览量
        request = requests.get(self.url + "/luka/api/user/kol/discover_detail", headers=self.header,
                               params={"discoverId": self.id, "on_shelf": "true"})
        if request.status_code != 200:
            print('discover_pv:' + "请求失败")
            return
        time.sleep(0.2)

    def water_army(self):
        # 获取水军列表
        request = requests.get(self.url + '/luka/api/water/getWaterUser', headers=self.header,
                               params={'limit': str(self.user_number), 'pageNo': 0})
        if request.status_code != 200:
            print("water_army: " + str(request.status_code))
            return
        t_list = re.findall('"uid" : "(.+?)"', str(request.text))
        time.sleep(1)
        return t_list

    def discover_csv(self, User_list):
        # 文本写入一条数据 评论id、评语、等待时间
        random_time = timeclass.latency_time(self)
        user = number(User_list)
        discover_type = self.item["discover_type"]
        kol_tpye_id = self.item["kol_tpye_id"]
        discover_text = self.item["discover_text"]
        test1 = comment()
        # discover_type: 发现类型       kol_tpye_id: 大咖类型       # discover_text: 发现文本字段
        a = test1.test(int(discover_type), kol_tpye_id, discover_text)
        text_comments = test1.if_contain_symbol(a)
        with open(self.file, "a+", newline="", encoding='utf-8') as f:
            k = csv.writer(f, dialect="excel")
            k.writerow([str(self.id), str(user), str(text_comments), str(random_time)])
        print("评论id：" + str(self.id) + " 评语：" + str(text_comments) + " 等待时间：" + str(random_time))

    def sort_csv(self):
        # 按照等待时间排序文本的时间从小到大
        data = csv.reader(open(self.file, encoding='utf-8'), delimiter=',')
        sortedlist = sorted(data, key=lambda x: int(x[3]), reverse=False)
        with open(self.file, "w", newline='', encoding='utf-8') as f:
            fileWriter = csv.writer(f, delimiter=',')
            for row in sortedlist:
                fileWriter.writerow(row)

    # 使用大咖id获取所有发现id
    def discover_id(self, kol_id):
        ids = []
        for id in kol_id:
            try:
                request = requests.get(self.url + "/luka/api/user/kol/discover_list", headers=self.header,
                                       params={"kolId": id, "pageNo": 0, "limit": 100})
                if request.status_code != 200:
                    print(request.text)
                    print('discover_page失败')
                    return
                a = request.json()['dt']
                sd = []
                for i in range(len(a)):
                    ids.append(a[i]["id"])
                    sd.append(a[i]["id"])
                    time.sleep(1)
                print(sd)
            except Exception as e:
                print("异常", e)
                time.sleep(3)
                request = requests.get(self.url + "/luka/api/user/kol/discover_list", headers=self.header,
                                       params={"kolId": id, "pageNo": 0, "limit": 100})
                if request.status_code != 200:
                    print(request.text)
                    print('discover_page失败')
                    return
                a = request.json()['dt']
                sd = []
                for i in range(len(a)):
                    ids.append(a[i]["id"])
                    sd.append(a[i]["id"])
                    time.sleep(1.2)
                print(sd)
                continue
        print(len(ids), ids)
        return ids

    # 获取全部列表的大咖id
    @retry(stop_max_attempt_number=3)
    def kol_list(self):
        request = requests.get(self.url + "/luka/api/user/kolIdAndNamesByType", headers=self.header,
                               params={"typeId": 0})
        if request.status_code != 200:
            print("出错")
            return
        r = request.json()["dt"]
        # print(len(r))
        c = []
        for i in range(len(r)):
            c.append(r[i]["uid"])
        c.append('7003946')
        return c


# if __name__ == "__main__":
#     # 发现执行id列表
#     # discoverID_list = []
#     user_number = 1000
#     file = "../Comment_csv/评论"+str(timeclass().current()[0])+".csv"
#     th = Threadgroup_1(None, user_number, file)
#     th.git_Cookie()
#     # 所有大咖分类列表
#     kol_id_list = th.kol_list()
#     discoverID_list = th.discover_id(kol_id_list)
#     cc = th.kol_typelist()
#     shuijunIDlist = th.water_army()
#     for i in discoverID_list:
#         time.sleep(1)
#         th = Threadgroup_1(i, user_number, file)
#         th.git_Cookie()
#         th.discover_page(cc, shuijunIDlist)
#         print(th.item)
#     th.sort_csv()

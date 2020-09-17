# !/opt/python37/bin/python3
# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
import copy
from data.time_class import *
import csv
from data.comment_test import *


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
        self.url = "http://test.pandacase.cn"

    def git_Cookie(self):
        # 获取Cookie
        request = requests.get(self.url + "/luka/api/user/login", headers=self.header,
                               params={"uid": 1258571561642934272, "pswd": "k4B5Xy"})
        if request.status_code != 200:
            print('git_Cookie:' + "请求失败")
            return
        b = request.headers
        session = re.findall(r"'luka-session': '(.+?)'", str(b))[0]
        cookie = re.findall(r"'Set-Cookie': '(.+?)'", str(b))[0]
        self.header["luka-session"] = session
        self.header["Set-Cookie"] = cookie
        time.sleep(0.2)
        return copy.deepcopy(self.header)

    def discover_page(self, cc, shuijunIDlist):
        # 返回需要评论条数
        request = requests.get(self.url + "/luka/api/user/kol/discover_detail", headers=self.header,
                               params={"discoverId": self.id, "on_shelf": "true"})
        if request.status_code != 200:
            print('discover_page:' + "----------请求失败ID:", self.id)
            return
        if re.findall(r'"ss" : (.+?)\n', request.text)[0] == "false":
            print("大咖发现不存在")
            return
        em = request.json()
        self.item["id"] = self.id
        self.item["vc"] = em['dt']['vc']
        self.item["cc"] = em['dt']['cc']
        self.item["discover_type"] = em['dt']['t']
        self.item["kolUser"] = em['dt']['userId']
        element_text = em["dt"]["chtml"]
        a = re.sub(r'<.+?>|“|”|&(.+?);', "", element_text)
        c = re.sub(r'。|\.|,', "，", a)
        g = c.split("，")
        for i in g:
            if len(i) < 10 or len(i) > 100:
                g.remove(i)
        if len(g) > 30:
            self.item["discover_text"] = g
        else:
            self.item["discover_text"] = []
        vc_1 = int(self.item["vc"]) / 100
        if int(vc_1) > int(self.item["cc"]) and int(self.item["vc"]) < 10000:
            cc_add = int(vc_1) - int(self.item["cc"])
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
        time.sleep(0.2)
        self.kol_user(cc, shuijunIDlist)
        return self.header

    def kol_user(self, cc, shuijunIDlist):
        # 用大咖id获取大咖的名字
        request = requests.get(self.url + '/luka/api/user/kol_detail?kolId=' + self.item["kolUser"])
        # print(request.text)
        if request.status_code != 200:
            print('kol_user:' + "请求失败")
            print(request.text)
            return
        elment = request.text
        self.item["kol_name"] = re.findall(r'"dn" : "(.+?)",', elment)[0]
        time.sleep(0.2)
        self.kol_tpye(cc, shuijunIDlist)
        return self.header

    def kol_typelist(self):
        # 获取所有type分类的内容
        kol_type = {}
        for i in range(1, 8):
            request = requests.get(self.url + '/luka/api/user/kolIdAndNamesByType', params={"typeId": i})
            kol_type[i] = request.text
        return kol_type

    def kol_tpye(self, cc, shuijunIDlist):  # -----------------------------------
        for s in range(self.item["commentID_number"]):
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
                               params={'limit': str(self.user_number), 'pageNo': 1})
        if request.status_code != 200:
            print("water_army: " + str(request.status_code))
            return
        t_list = re.findall('"uid" : "(.+?)"', str(request.text))
        time.sleep(0.5)
        return t_list

    def discover_csv(self, User_list):
        # 文本写入一条数据 评论id、评语、等待时间
        random_time = timeclass.latency_time(self)
        user = number(User_list)
        discover_type = self.item["discover_type"]
        kol_tpye_id = self.item["kol_tpye_id"]
        discover_text = self.item["discover_text"]
        test1 = comment()
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


if __name__ == "__main__":
    # 发现执行id列表
    discoverID_list = [32, 33, 51, 55, 59, 60]
    user_number = 120
    file = "../Comment_csv/评论次数2.csv"
    th = Threadgroup_1(None, user_number, file)
    th.git_Cookie()
    cc = th.kol_typelist()
    shuijunIDlist = th.water_army()
    for i in discoverID_list:
        time.sleep(1)
        th = Threadgroup_1(i, user_number, file)
        th.git_Cookie()
        th.discover_page(cc, shuijunIDlist)
        print(th.item)
        print("")
    th.sort_csv()
    time.sleep(10)

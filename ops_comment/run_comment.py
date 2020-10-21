from ops_comment.ops_pv import *
from ops_comment.ops_csvtest import *
from data.comment_test import *
from data.time_class import *
import os.path


class Run:
    def pv_run(self):
        user_number = 1000
        file = "../Comment_csv/评论" + str(timeclass().current()[0]) + ".csv"
        th = Threadgroup_1(None, user_number, file)
        th.git_Cookie()
        # 所有大咖分类列表
        kol_id_list = th.kol_list()
        discoverID_list = th.discover_id(kol_id_list)
        cc = th.kol_typelist()
        shuijunIDlist = th.water_army()
        for i in discoverID_list:
            time.sleep(1)
            th = Threadgroup_1(i, user_number, file)
            th.git_Cookie()
            th.discover_page(cc, shuijunIDlist)
            # print(th.item)
        th.sort_csv()  # 时间排序

    def csvtest_run(self, file):
        if os.path.isfile(file):
            def comment_csv_list():
                data = csv.reader(open(file, encoding='utf-8'), delimiter=',')
                sortedlist = sorted(data, key=lambda x: int(x[3]))
                return sortedlist

            b = comment_csv_list()
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
        else:
            print("评论csv文件不存在")


if __name__ == '__main__':
    file = "../Comment_csv/评论" + str(timeclass().current()[0]) + ".csv"
    if os.path.isfile(file):
        Run().csvtest_run(file)
    else:
        try:
            Run().pv_run()
            time.sleep(10)
            Run().csvtest_run(file)
        except Exception as e:
            print(e)

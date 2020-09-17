import json
import os
import csv

path = "D:\gitlibrary\公司\dicover_script\comment_script\json文件"
filelist = os.listdir(path)
for i in filelist:
    with open(path + "\\" + i, 'r') as load_f:
        load_dict = json.load(load_f)
    # print(load_dict)

    for j in load_dict["result"]["books"]:
        with open("叶老师书房信息.csv", "a+", newline="", encoding='utf-8') as f:
            k = csv.writer(f, dialect="excel")
            k.writerow([j["name"], j["author"], j["isbn"], j["img"]])

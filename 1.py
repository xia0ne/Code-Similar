import os
import sys
import re
import time
import pypinyin
import json
import socket
import zipfile
import http
import socket


class Code:
    def __init__(self, Code_source, dir_name, out_file):
        self.Code_source = Code_source
        self.dir_name = dir_name
        self.out_file = out_file
        self.file_name = []
        self.Quetion_num = []

    def get_file_name(self):
        # print('正在获取文件名')
        for files in os.walk(self.Code_source + self.dir_name):
            for file in files:
                self.file_name.append(file)
        for file in self.file_name[2]:
            with open(self.Code_source + file, 'a+') as f:
                # 输出换行符
                f.write('\n')

    def get_question_num(self, file_name):
        return re.findall('[A-Z](?=\.txt)', file_name)

    def get_Pinyin(self, str):
        # pinyin_list = pypinyin.pinyin(str, style=pypinyin.NORMAL)
        # pinyin_str = ''
        # for pinyin in pinyin_list:
        #     pinyin_str += pinyin[0]
        # return pinyin_str
        return str

    def Probelms_Handle(self):
        for name in self.file_name[2]:
            question_num = self.get_question_num(name)
            if (question_num not in self.Quetion_num):
                self.Quetion_num.append(question_num)
            if not os.path.exists(self.Code_source + question_num[0]):
                os.makedirs(self.Code_source + question_num[0])
            with open(self.Code_source + self.dir_name + name, 'r', encoding='utf-8') as f:
                with open(self.Code_source + question_num[0] + '\\' + self.get_Pinyin(name), 'w', encoding='utf-8') as f1:
                    f1.write(f.read())
                    f1.write('\n')

    def get_sim_command(self, question_num):
        if not os.path.exists(self.out_file):
            os.makedirs(self.out_file)
        sim_path = "SSSIM\\"
        cil = sim_path + "sim_c.exe -p -s -e " + \
            self.Code_source + question_num[0]
        for question in os.walk(self.Code_source + question_num[0]):
            for file in question[2]:
                cil += ' ' + self.Code_source + question_num[0] + '\\' + file
        cil += ' > ' + self.out_file + question_num[0] + '.txt'
        os.system(cil)

    def getOri(self,pinyin):
        for name in self.file_name[2]:
            now_name = name[:-12]
            if (self.get_Pinyin(now_name) == pinyin):
                return now_name
    # 将结果生成json文件
    def get_json(self):
        js = {}
        for question_num in self.Quetion_num:
            cnt = 0
            with open(self.out_file + question_num[0] + '.txt', 'r') as f:
                # print('正在处理' + question_num[0])
                if(question_num[0] == 'A'):
                    continue 
                result = f.read()
                regexIter = re.finditer(r".*\\(.+?)_(.*?[A-Z])\.txt.*?(\d+)\s?%.*\\(.+?)_(.*?[A-Z])", result, re.MULTILINE)
                for match in regexIter:
                    if match.group(2) not in js:
                        js[match.group(2)] = {}
                    if cnt not in js[match.group(2)]:
                        js[match.group(2)][cnt] = {}
                    if((int)(match.group(3)) < 70):
                        continue
                    # unicode转中文
                    js[match.group(2)][cnt]["author1"] = self.getOri(match.group(1))
                    js[match.group(2)][cnt]["author2"] = self.getOri(match.group(4))
                    js[match.group(2)][cnt]["percent"] = match.group(3)
                    cnt += 1
        # print(js)
        with open(self.out_file + 'result.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(js).encode('utf-8').decode('unicode_escape'))
    def dejson(self):
        with open(self.out_file + 'result.json', 'r', encoding='utf-8') as f:
            with open(self.out_file + 'result.txt', 'w', encoding='utf-8') as f1:
            # js = json.load(f)
            # for key in js:
            #     print(key)
            #     for value in js[key]:
            #         print(value)
            #         print(js[key][value])
                js = json.load(f)
                for key in js:
                    f1.write(key + ":\n")
                    for value in js[key]:
                        for key1 in js[key][value]:
                            f1.write(js[key][value][key1] + " ")
                        f1.write("\n")
                    f1.write("----------------------------\n")

    def Main(self):
        self.get_file_name()
        self.Probelms_Handle()
        for question_num in self.Quetion_num:
            self.get_sim_command(question_num)
            print("正在处理第" + question_num[0] + "题")
        # print(self.file_name)
        # self.get_json()
        # self.dejson()


def main():
    # 总用时
    start = time.time()
    code = Code('COde\\','original\\','Ans\\')
    code.Main()
    end = time.time()
    print('总用时：' + str(end - start))
    # 服务器
    # server = Server('127.0.0.1', 8888)
    # server.Main()
    # http服务器
    # httpserver = HttpServer(8888)


if __name__ == '__main__':
    main()

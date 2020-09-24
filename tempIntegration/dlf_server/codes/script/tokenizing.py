from konlpy.tag import Okt
import os
import csv
import pickle

okt = Okt()

content = ""

# ==== 형태소 분석 ====
# cf = open("data_output.csv",mode="r")
# cfreader = csv.reader(cf,delimiter=",")
# wcf = open("data_tokenized.csv",mode = "w")
# wcfwriter = csv.writer(wcf)

# for row in cfreader:
#     res = okt.pos(row[0])
#     for word in res:
#         lst = []
#         if word[1] == "Noun":
#             lst.append(word[0])
#             lst.append(row[1])
#             wcfwriter.writerow(lst)

# cf = open("data_tokenized.csv",mode = "r")
# cfreader = csv.reader(cf,delimiter=",")
# dict = dict()
# for row in cfreader:
#     key = row[0]
#     val = row[1]
#     if str(key) not in dict:
#         dict[str(key)] = []
#     dict[str(key)].append(val)

# fw = open('script_word.pickle','wb')
# pickle.dump(dict,fw)

# fr = open('script_word.pickle','rb')
# loaded = pickle.load(fr)

# print(len(loaded['제일']))
data = dict()
data['contents'] = ">안녕"
if len(data['contents'])>0 and data['contents'][0]=='>':
    print(data['contents'])
    print(data['contents'][1:])
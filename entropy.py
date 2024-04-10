import math
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import jieba
from collections import Counter
start_time = time.time()
# 读取停顿词数据
with open('cn_stopwords.txt', 'r', encoding='utf-8') as file:
    stopwords = file.read().splitlines()
# 读取所有中文文本数据并合并
file_directory = r'D:\dpwork\data'
merged_text = ""
for file_name in os.listdir(file_directory):
    if file_name.endswith(".txt"):
        with open(os.path.join(file_directory, file_name), 'r', encoding='utf-8') as file:
            text = file.read()
            merged_text += text
merged_text = merged_text.replace("\n", "")
merged_text = merged_text.replace("\u3000", "")
merged1_text = merged_text.replace(" ", "")
merged_text = [word for word in merged1_text if word not in stopwords]
words_text = jieba.cut(merged1_text)
words_text = [word for word in words_text if word not in stopwords]
#word_freq = Counter(words_text)
def chinese_entropy1(text):
    frequency = {}
    total = 0
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
        total += 1

    entropy = 0
    for count in frequency.values():
        probability = count / total
        entropy -= probability * math.log(probability, 2)
    return entropy

def chinese_entropy2(text):

    bigrams = [(text[i], text[i+1]) for i in range(len(text)-1)]

    bigram_count = Counter(bigrams)
    total_bigrams = len(bigrams)

    entropy = 0
    frequency = {}
    total = 0
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
        total += 1
    for bigram,count in bigram_count.items():
        p_xy = count / total_bigrams
                #bigram[1] / total_bigrams)  # 联合概率p(xy)
        a=frequency[bigram[0]]
        p_x_y = count / frequency[bigram[0]]  # 条件概率p(x|y)
        entropy -= p_xy * math.log(p_x_y, 2)

    return entropy
def chinese_entropy3(text):

    bigrams = [(text[i], text[i+1]) for i in range(len(text)-1)]
    bigram_count = Counter(bigrams)
    total_bigrams = len(bigrams)

    trigrams = [(text[i], text[i + 1], text[i + 2]) for i in range(len(text) - 2)]  # 手动创建三元组
    trigram_count = Counter(trigrams)
    total_trigrams = len(trigrams)  # 获取三元组的总数

    entropy = 0
    for trigram, count in trigram_count.items():
        p_xyz = count / total_trigrams  # 计算三元组的联合概率


        p_xy_z = count / bigram_count[(trigram[0],trigram[1])]  # 计算条件概率
        entropy -= p_xyz * math.log(p_xy_z, 2)#条件概率p(x|y)
    return entropy

entropy1_0 = chinese_entropy1(merged_text)
entropy1_1 = chinese_entropy1(words_text)
entropy2_0 = chinese_entropy2(merged_text)
entropy2_1 = chinese_entropy2(words_text)
entropy3_0 = chinese_entropy3(merged_text)
entropy3_1 = chinese_entropy3(words_text)
print("一元字信息熵为:", entropy1_0)
print("一元词信息熵为:", entropy1_1)
print("二元字信息熵为:", entropy2_0)
print("二元词信息熵为:", entropy2_1)
print("三元字信息熵为:", entropy3_0)
print("三元词信息熵为:", entropy3_1)
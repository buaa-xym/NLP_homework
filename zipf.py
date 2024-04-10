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
merged_text = merged_text.replace(" ", "")
words = jieba.cut(merged_text)

# 过滤停顿词
filtered_words = [word for word in words if word not in stopwords]

# 统计词频
word_freq = Counter(filtered_words)

# 根据词频排序
word_freq = dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True))

# 获取词频的排名和词频数
ranks = list(range(1, len(word_freq) + 1))
freqs = list(word_freq.values())
# 输出出现频率最高的前几个词语
num_top_words = 100
top_words = dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True)[:num_top_words])
print(top_words)
with open('save\data.txt', 'w', encoding='utf-8') as file:
    file.write('前{}个数据\n'.format(num_top_words))
    i = 1
    for item,value in top_words.items():
        file.write( str(item) +' '+'排名:'+str(i)+'频率:'+str(value) +'\n')
        i += 1
plt.figure(figsize=(10, 6))


plt.loglog(ranks, freqs, color='b', linestyle='--')

plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.title("Zip's Law")
plt.legend()
plt.show()

plt.savefig('11.png')
end_time = time.time()
run_time = end_time - start_time
print(f"程序运行时间为：{run_time} 秒")

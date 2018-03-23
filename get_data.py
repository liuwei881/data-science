# coding=utf-8


import sys, re
# sys.argv是命令行参数的列表
# sys.argv[0]是程序自己的名字
# sys.argv[1]会是在命令行上指定的正则表达式
# 对传递到这个脚本中的每一个行
# 如果它匹配正则表达式，则把它写入stdout

regex = sys.argv[1]
for line in sys.stdin:
    if re.search(regex, line):
        sys.stdout.write(line)


import sys
count = 0
for line in sys.stdin:
    count += 1
print(count)

import sys
from collections import Counter
# 传递单词的个数作为第一个参数
try:
    num_words = int(sys.argv[1])
except:
    print("usage: most_common_words.py num_words")
    sys.exit(1)
counter = Counter(word.lower() for line in sys.stdin if word)
for word, count in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout.write("\n")
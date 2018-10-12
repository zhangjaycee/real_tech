#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
by Jaycee 20181012,
refs: https://blog.csdn.net/u010309756/article/details/67637930
      https://blog.csdn.net/wireless_com/article/details/60571394
'''

import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba


# stop word
rm_list = [u"可以", u"一个", u"进行", u"使用", u"需要", \
           u"http", u"html", u"如果", u"这个", u"支持", \
           u"比如", u"这样", u"操作", u"或者", u"就是", \
           u"对于", u"但是", u"可能", u"命令", u"选项", \
           "https", "html", u"导致", u"没有", u"类似", \
           u"一些", u"所以", u"问题", u"对应", u"我们", \
           u"不同"]


# read all texts from my Wiki
all_text = ""
for root,dirs,files in os.walk('.'):
    for f in files:
        if f[-3:] == ".md":
            path = os.path.join(root, f)
            all_text += open(path).read()

# cut texts by jieba
wordlist_jieba = jieba.cut(all_text, cut_all = True)

# stop word filter
word_list = []
append_count = 0
rm_count = 0
for i in wordlist_jieba:
    if i not in rm_list:
        word_list.append(i) 
        append_count += 1
    else:
        rm_count += 1
print "Number of word we have removed:", rm_count 
print "Number of word remained:", append_count
final_text = " ".join(word_list)

# genertate word cloud
# colormap can be set: 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
fontpath="PingFang.ttc"
my_wordcloud = WordCloud(font_path=fontpath, width=1080, height=720, \
                         background_color='white', relative_scaling=1, \
                         max_words=66, min_font_size=12, colormap="inferno" ).generate(final_text)

# show
#plt.imshow(my_wordcloud)
#plt.axis("off")
#plt.show()

# save
my_wordcloud.to_file('wordcloud.jpg')


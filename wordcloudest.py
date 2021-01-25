# -*- coding = utf-8 -*-
# @Time : 2021/1/25 11:10
# @Author : 费佳伟
# @File : wordcloudest.py
# @Software : PyCharm

# 方正粗黑宋简体.ttf
import numpy as np
from PIL import Image
import re
import jieba
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

path = r'D:\\python_test\\'
content = 'D:\\python_test\\'+'央视新闻2020-1.txt'
# 打开存放项目名称的txt文件
with open(content, 'r', encoding='utf-8') as f:
    word = (f.read())
    f.close()


# 图片模板和字体
image = np.array(Image.open(path+'virus.jpg'))
font = r'C:\\Windows\\Fonts\\方正粗黑宋简体.ttf'

# 去掉英文，保留中文
resultWord = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\。\@\#\\\&\*\%]", "", word)
wordlist_after_jb = jieba.cut(resultWord)
wl_space_split = " ".join(wordlist_after_jb)

# 设置停用词
sw = set(STOPWORDS)
sw.add("等人")
sw.add("回复")
sw.add("共")
sw.add("条")
sw.add("共条")
sw.add("等")
sw.add("人")
sw.add("的")
sw.add("小")
sw.add("啊")
sw.add("呀")
sw.add("吧")
sw.add("吗")
sw.add("了")
sw.add("不")
sw.add("没有")
sw.add("能")
sw.add("不能")
sw.add("知道")
sw.add("和")
sw.add("我们")
sw.add("他们")
sw.add("你们")
sw.add("可以")
sw.add("也")
sw.add("我")
sw.add("我是")
sw.add("是")
sw.add("今天")
sw.add("都在")
sw.add("就")
sw.add("在")
sw.add("真的")
sw.add("大家")
sw.add("都")
sw.add("来")
sw.add("这")
sw.add("这些")
sw.add("但")
sw.add("但是")
sw.add("你")
sw.add("大")
sw.add("还")
sw.add("让")
sw.add("去")
sw.add("一")
sw.add("现在")
sw.add("应该")
sw.add("才")
sw.add("有")
sw.add("请")
sw.add("要")
sw.add("啦")
sw.add("哦")
sw.add("个")
sw.add("一个")
sw.add("觉得")
sw.add("因为")
sw.add("每天")
sw.add("什么")
sw.add("时候")
sw.add("一定")
sw.add("用")
sw.add("想")
sw.add("说")
sw.add("那些")
sw.add("哈哈")
sw.add("哈哈哈")
sw.add("为什么")
sw.add("感觉")
sw.add("好")


# 关键一步
my_cloud = WordCloud(scale=4,
                     font_path=font,
                     width=1000,
                     height=800,
                     mask=image,
                     stopwords=sw,
                     background_color='white',
                     max_words=200,
                     max_font_size=200,
                     random_state=20).generate(wl_space_split)

# 显示生成的词云
plt.imshow(my_cloud)
plt.axis("off")
plt.show()

# 保存生成的图片
my_cloud.to_file(path+'央视新闻2020-1.jpg')

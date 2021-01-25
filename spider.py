# -*- coding = utf-8 -*-
# @Time : 2021/1/19 17:09
# @File : spider.py
# @Software: PyCharm

import urllib.request
import xlwt
from bs4 import BeautifulSoup
import re
import pandas as pd
import jieba
from pyhanlp import HanLP

findlink=re.compile(r'<a href="(.*?)" ')
def main():
    #1. 爬取网页
    baseurl="http://news.sina.com.cn/head/news202006"
    datalist=[]
    datalist=getData(baseurl)
    savepath = "202006.xls"
    #3.保存数据
    SaveData(datalist,savepath)


#爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(1,27):
        if i<10:
            url=baseurl+str("0"+str(i)+"am.shtml")
        else:
            url = baseurl+str(str(i)+"am.shtml")
        html=askURL(url)
        soup= BeautifulSoup(html, "html.parser")
        data1=soup.select("#ad_entry_b2 ")
        for item in data1:
            item=str(item)
            for i in range(0,len(re.findall(findlink, item))):
                link=re.findall(findlink, item)[i]
                if str(link).startswith("https://news.sina.com.cn/"):
                    #print(link)
                    data2=Analaysis(link)
                    datalist.append(data2)
                else:
                    continue
        data=soup.select("#syncad_1")
        for item in data:
            item=str(item)
            for i in range(0,len(re.findall(findlink, item))):
                link=re.findall(findlink, item)[i]
                if str(link).startswith("https://news.sina.com.cn/"):
                    #print(link)
                    data3=Analaysis(link)
                    datalist.append(data3)
                else:
                    continue
    return datalist


# 得到一个指定url的网页内容
def askURL(url):
    head={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html=""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        print("fail")
    return html

#解析指定新闻
def Analaysis(url):
    global articleall
    datalist=[]
    html=askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    try:
        title=soup.select('.main-title')[0].text #标题
        datalist.append(title)
        timesource = soup.select('.date-source span')[0].text #时间
        datalist.append(timesource)
        article = []  # 获取文章内容
        for p in soup.select('.article p')[:-1]:
            article.append(p.text.strip())
            articleall = ' '.join(article)
        datalist.append(articleall)
        print(datalist)
        return datalist
    except IndexError as e:
        datalist=["fail","fail","fail"]
        print("fail")
        return datalist
        #pass


#保存数据
def SaveData(datalist, savepath):
    workBook = xlwt.Workbook(encoding="utf-8")
    worksheet = workBook.add_sheet('sheet1',cell_overwrite_ok=True)
    col=("title", "time", "article")
    for i in range(0,3):
        worksheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        for j in range(0, 3):
            worksheet.write(i+1,j,datalist[i][j])
    workBook.save(savepath)


#excel转换成txt方便处理
#df = pd.read_excel('202006.xls', sheet_name='sheet1', header=None)		# 使用pandas模块读取数据
#print('开始写入txt文件...')
#df.to_csv('file202006.txt', header=None, sep=',', index=False)		# 写入，逗号分隔
#print('文件写入成功!')


txt=open("file202006.txt","r",encoding="utf-8").read()
words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
counts = {}  # 通过键值对的形式存储词语及其出现的次数
PassWord=['中国','美国','香港','我们','一个','问题','报道','国家','表示','他们','没有','自己','标题','进行','记者'
    ,'警方','已经','这个','今年','可以','就是','通过','这些','媒体','认为','可能','世界','一些','社会','国际',
          '企业','公司','俄罗斯','情况','发现','政治','时间','如果','不是','中方','书记','开始','调查','政府','这样','要求',
          '重要','其中','目前','总统','什么','成为','作为','有关','相关','因为','新闻','发生','关系','还是','显示','现在',
          '网友','希望','习近平','支持','活动','工作','伊朗','武汉','病例','确诊','医院','社区','日本','人员','新型','疫情'
         ,'湖北','信息','特朗普','新冠','病毒','发展','英国','印度','北京','肺炎','患者','组织','出现']
for word in words:
    if word in PassWord:  #在停词表内的词跳过
        continue
    if len(word)==1 : # 单个字符的词跳过
        continue
    if str(word).isdigit(): #是数字的也跳过
        continue
    if str(word)=="fail": #因为上面出现异常时写入的是fail，所以fail也需要跳过
        continue
    else:
        counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

items = list(counts.items())  # 将键值对转换成列表
items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序
f=open('202006top10.txt','w') # 写入相应的txt文件中
for i in range(10):
    word, count = items[i]
    print("{0:<5}{1:>5}".format(word, count),file=f)
f.close()

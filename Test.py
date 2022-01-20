# -*- coding: UTF-8 -*-
import urllib.request

import re

import pandas as pd
import pymysql

import time


def sinaStockUrl(pageNum):
    print('pageNum : ' + str(pageNum))

    rows = 10

    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?'
    url += 'page=' + str(pageNum)
    url += '&num=' + str(rows)
    url += '&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=init'

    print(url)

    return url


def sinaStockData(url):
    # http://www.cnblogs.com/sysu-blackbear/p/3629420.html
    stockDataResponse = urllib.request.urlopen(url)
    stockData = stockDataResponse.read()
    # stockData = stockDataResponse.decode('utf8')
    # stockData = stockData.decode('gbk')
    stockData = stockData.decode('gb2312')

    print(stockData)

    return stockData

# 在地址里symbol指的是股票代码，这里需要注意的是不能只填数字代码，还需要把交易市场的前缀加上去，比如sz000001指的是平安银行，
# 而sh000001则是上证指数；
# scale表示的是时间长度，以分钟为基本单位，输入240就表示下载日K线数据，
# 60就是小时K线数据，貌似最短时间是5分钟，并没有提供分钟数据；
# datalen则是获取数据的条数，在日K线的时间长度了，
# datalen就是获取60天日K数据，当然也可以获取60小时K数据。
#sinaStockData((sinaStockUrl(240)))
url ="https://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var=/CN_MarketData.getKLineData?symbol=sz000001&scale=15&ma=no&datalen=10"
page = urllib.request.urlopen(url)
html = page.read()
html = html.decode("gbk")
print("原始字符","="*50)
# print(html)
tmpHtml =html[html.index("var=(")+len("var=("):]
final_html =tmpHtml[:len(tmpHtml)-2]
final_html=eval(final_html)
print("原始字符",type(final_html))
print(final_html)
df = pd.DataFrame(final_html)
# print("df=================================================================df====================================================================df")
# print(df)
# print("datalist...........................................................datalist................................................................datalist")
# # print(final_html)
# for i in range(len(final_html)):
#     all_item = final_html[i].split(',')
#     print(all_item)


print("=getdata===============================================================================================================================")

def getdata(code,scale,datalen):
    links = 'http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var=/CN_MarketData.getKLineData?symbol=' + code + '&scale=' + str(scale) + '&ma=no&datalen='+str(datalen)
    histData = urllib.request.urlopen(links).read()
    histData = str(histData).split('[')[1]
    histData = histData[1:len(histData) - 4].split('},{')
    datas = []
    for i in range(0, len(histData)):
        column = {}
        dayData = histData[i].split(',')
    for j in range(0, len(dayData)):
        field = dayData[j].split(':"')
        if field[0] == 'day':
            column['date'] = field[1].replace('"', '')
        else:
            column[field[0]] = field[1].replace('"', '')

        datas.append(column)

    return datas
dfata = getdata("sz000001",240,10)
print(dfata)
df = pd.DataFrame(dfata)
print(df)
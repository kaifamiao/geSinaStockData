# -*- coding: UTF-8 -*-
import urllib.request

import re

import pandas as pd
import pymysql

import time,datetime
pd.set_option('display.expand_frame_repr', False)

from colorama import init, Fore, Back, Style
init(autoreset=True)
def get_data(ts_code,scale,datalen,encoding="gbk",):
    # 在地址里symbol指的是股票代码，这里需要注意的是不能只填数字代码，还需要把交易市场的前缀加上去，比如sz000001指的是平安银行，
    # 而sh000001则是上证指数；
    # scale表示的是时间长度，以分钟为基本单位，输入240就表示下载日K线数据，
    # 60就是小时K线数据，貌似最短时间是5分钟，并没有提供分钟数据；
    # datalen则是获取数据的条数，在日K线的时间长度了，
    # datalen就是获取60天日K数据，当然也可以获取60小时K数据。
    # sinaStockData((sinaStockUrl(240)))
    url = "https://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var=/CN_MarketData.getKLineData?"
    url += "symbol="+ts_code+"&scale="+str(scale)+"&ma=no&datalen="+str(datalen)
    print(url)
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode(encoding)
    # print("原始字符","="*50)
    # print(html)
    tmpHtml = html[html.index("var=(") + len("var=("):]
    final_html = tmpHtml[:len(tmpHtml) - 2]
    final_html = eval(final_html)
    # print("原始字符",type(final_html))
    # print(final_html)
    df = pd.DataFrame(final_html)
    df['trade-date'] = df.day.astype('str').str[0:10]
    df['trade-time'] = df.day.astype('str').str[10:len(df.day)]
    period="日线"
    if scale==240:
        period = "日线"
    if scale==5:
        period = "5MIN"
    if scale==15:
        period = "15MIN"
    if scale==30:
        period = "30MIN"
    if scale==60:
        period = "60MIN"
    df['period'] = period

    df.insert(0,"ts_code",ts_code,allow_duplicates=False)
    # df.drop([len(df) - 1], inplace=True)
    df.drop(['day'], axis=1,inplace=True)
    return df


if __name__ == '__main__':
    # print("program is running....")
    print("程序开始运行。。。")
    # 统计程序开始时间
    starttime = datetime.datetime.now()
    print("df=================================================================df===================================df")
    df = get_data("sz000518",5,2000)


    print(df)
    print("df=================================================================df===================================df")
    # 统计程序开结束时间
    endtime = datetime.datetime.now()
    print("\n程序运行时间：" + str(endtime - starttime))
    print('=============================\t程序运行结束\t=============================')

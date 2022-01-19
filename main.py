# -*- coding: UTF-8 -*-
import os
import re,sys,urllib.request,time
import pandas as pd
from Tools import printinfo
pd.set_option('display.expand_frame_repr', False)

from colorama import init, Fore, Back, Style
init(autoreset=True)

class SinaData:
    #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////get_data strat......
    def get_data(self):
        print("get_Data()")
        i=0
        list =self.getlist()
        printinfo("list："+list[4698],"YELLOW")
        codelist=""
        print("list count",len(list))

        step = 800
        total_count = len(list)

        # step = 4
        # total_count = 8 #len(list)


        if total_count % step ==0:
            kkkk = total_count / step
            print("整除kkkk:=", kkkk)
        else:
            kkkk = total_count / step+1
            print("未整除kkkk:=", kkkk)

        kkkk =int(kkkk)

        # 总循环次数：6
        # 0x := 0y := 800
        # 1x := 800y := 1600
        # 2x := 1600y := 2400
        # 3x := 2400y := 3200
        # 4x := 3200y := 4000
        # 5x := 4000y := 4800
        printinfo("总循环次数：" + str(kkkk), "RED")
        printinfo("总记录total_count：" + str(total_count), "RED")
        # for i in range(kkkk):
        #
        #     x=step*i
        #     y=step*(i+1)
        #     print("["+str(i)+"]", "=============================================================", "x:=", x, "y:=", y)
        #
        #     for z in range(x,y):
        #         print(z)
        #
        #     # time.sleep(5)
        #     # os.system("cls")
        tmp=0
        y=step
        #////循环开始///////////////////////////////////////////////////////////////////////////////////////////////////
        for i in  range(kkkk):
            codelist_final = ""
            if i % 2==0:
                COLORS = "MAGENTA"
            else:
                COLORS = "BLUE"
            x=tmp
            if i==kkkk-1:
                y=total_count
            else:
                y=step*(i+1)
            # print("["+str(i)+"]", "=============================================================", "x:=", x, "y:=", y)
            tmpxxx="["+str(i)+"]=================================================第（"+str(i+1)+"）次循环【x:="+ str(x)+ "\ty:="+ str(y) +"】============================================================="
            printinfo(tmpxxx,COLORS)
            self.outlog(tmpxxx)
            tmp =y

            for z in range(x,y):
                # printinfo(str(z),COLORS)
                if z<y-1:
                    codelist_final+=list[z]+","
                else:
                    codelist_final += list[z]

            self.outlog(codelist_final)
            # print(codelist_final)

            df = self.GetSinaALLData(codelist_final)
            # print("*" * 50, "GET print DF", "*" * 50)
            # print(df)
            print("i=",i)
            if i==0:
                ser =pd.concat([df,])
            else:
                ser=pd.concat([df,ser])
            # else:
            #     ser = pd.concat([ser, tmp])
            # tmp =df
            # print("X"*80,"print DF ","X"*80)
            # print(tmp)
            # time.sleep(3)

        # ////循环结束///////////////////////////////////////////////////////////////////////////////////////////////////
        print(Fore.RED+"=" * 50, Fore.RED+Back.YELLOW+Style.BRIGHT+"循环获取结束", Fore.RED+"=" * 50)
        print(ser)
        # ser.to_csv("DAY.csv")
        print(Fore.YELLOW+Back.BLUE+"整合后的df长度：【"+str(ser.shape[0])+"】")
        printinfo("="*150,"RED")
        # N=9
        # for k in range(N):
        #     # print(k)
        #     if k<N-1:
        #         codelist+=list[k]+","
        #     else:
        #         codelist += list[k]
        # #     # print(k,"sz000"+str(k))
        # SSSSSS= "codelist="+ str(len(codelist.split(",")))+ codelist
        # printinfo(SSSSSS,"RED")
        # df= self.GetSinaALLData(codelist)

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////get_data END......
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////getlist start/////////
    def getlist(self):
        df =pd.read_csv("stocklist.csv",converters={'symbol':str})

        # print(df["ts_code"].str.split('.', expand=True))
        codelist=df["symbol"].values.tolist()
        # print(codelist)

        lsit_str=[]
        print()
        for list in codelist:
            if list[0]=="0":
                lsit_str.append("sz"+list)
            if list[0]=="6":
                lsit_str.append("sh"+list)
            if list[0]=="8":
                lsit_str.append("bj"+list)
            if list[0]=="3":
                lsit_str.append("sz"+list)
            if list[0]=="4":
                lsit_str.append("bj"+list)
        # print(lsit_str)
        print("文件读取长度",len(codelist),"处理后长度",len(lsit_str),type(lsit_str))

        return lsit_str

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////getlist end/////////
    #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////GetSinaALLData===============
    def GetSinaALLData(self,stock_code):
        url = 'http://hq.sinajs.cn/list=' + stock_code.lower()
        # page = urllib3.urlopen(url)
        self.outlog(url)
        page = urllib.request.urlopen(url)
        html = page.read()
        html = html.decode("gbk")
        self.outlog("原始字符",html)
        # print(html)
        data = re.compile(r'="(.*?)";')
        datalist = re.findall(data, html)
        self.outlog("datalist",str(len(datalist)))

        #///////////////////////////////////////////////////
        #
        #/////////////
        stock_dict_list=[]
        print("总共：",len(datalist))
        sumCount=0
        for i in range(len(datalist)):
            all_item = datalist[i].split(',')
            ts_Code =stock_code.split(",")
            if len(all_item)>=10:
                sumCount+=1
                # print(i, "处理字符", all_item)
                self.outlog(str(i)+"处理字符:"+str(all_item))
                stock_dict = {}
                stock_dict['日期'] = all_item[30]
                stock_dict['时间'] = all_item[31]
                stock_dict['ts_code'] = ts_Code[i]

                stock_dict['股票名称'] = all_item[0]  # stock_name_final
                stock_dict['开盘价'] = all_item[1]
                stock_dict['昨日收盘'] = all_item[2]
                stock_dict['当前价格'] = all_item[3]
                stock_dict['最高价格'] = all_item[4]
                stock_dict['最低价格'] = all_item[5]
                stock_dict['买入价'] = all_item[6]
                stock_dict['卖出价'] = all_item[7]
                stock_dict['成交数量'] = all_item[8]
                stock_dict['成交金额'] = all_item[9]
                stock_dict['状态'] = all_item[32]

                stock_dict_list.append(stock_dict)

            # df.append(stock_dict)
        # print(stock_dict_list)
        print("实际数量",sumCount)
        df = pd.DataFrame(stock_dict_list)
        print("="*50,"\t GetSinaALLData DF \t","="*50)
        print(df)
        return df
        # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////GetSinaALLData End===============
    def GetSinaData(self,stock_code):
        # if stock_code[0] == '6':
        #     url = 'http://hq.sinajs.cn/list=sh' + stock_code
        # else:
        #     url = 'http://hq.sinajs.cn/list=sz' + stock_code
        url = 'http://hq.sinajs.cn/list=' + stock_code.lower()
        # page = urllib3.urlopen(url)
        print(url)
        page = urllib.request.urlopen(url)
        html = page.read()
        html = html.decode("gb2312")
        print("原始字符\n",html)
        data = re.compile(r'="(.*?)";')
        datalist = re.findall(data, html)
        all_item = datalist[0].split(',')
        print("处理字符",all_item)
        # stock_name_orig = all_item[0].decode("GB2312")
        # stock_name_final = stock_name_orig.encode("UTF-8")

        stock_dict = {}
        stock_dict['日期'] = all_item[30]
        stock_dict['时间'] = all_item[31]
        stock_dict['状态'] = all_item[32]
        stock_dict['股票名称'] = all_item[0]  # stock_name_final
        stock_dict['开盘价'] = all_item[1]
        stock_dict['昨日收盘'] = all_item[2]
        stock_dict['当前价格'] = all_item[3]
        stock_dict['最高价格'] = all_item[4]
        stock_dict['最低价格'] = all_item[5]
        stock_dict['买入价'] = all_item[6]
        stock_dict['卖出价'] = all_item[7]
        stock_dict['成交数量'] = all_item[8]
        stock_dict['成交金额'] = all_item[9]
        stock_dict['买1量'] = all_item[10]
        stock_dict['买1价'] = all_item[11]
        stock_dict['买2量'] = all_item[12]
        stock_dict['买2价'] = all_item[13]
        stock_dict['买3量'] = all_item[14]
        stock_dict['买3价'] = all_item[15]
        stock_dict['买4量'] = all_item[16]
        stock_dict['买4价'] = all_item[17]
        stock_dict['买5量'] = all_item[18]
        stock_dict['买5价'] = all_item[19]
        stock_dict['卖1量'] = all_item[20]
        stock_dict['卖1价'] = all_item[21]
        stock_dict['卖2量'] = all_item[22]
        stock_dict['卖2价'] = all_item[23]
        stock_dict['卖3量'] = all_item[24]
        stock_dict['卖3价'] = all_item[25]
        stock_dict['卖4量'] = all_item[26]
        stock_dict['卖4价'] = all_item[27]
        stock_dict['卖5量'] = all_item[28]
        stock_dict['卖5价'] = all_item[29]

        # for item in all_item:
        #

        #    print(item)

        return stock_dict

    def GetSinaData_pd(self,ts_code):
        dict =self.GetSinaData(ts_code)
        # print("dict\n", dict)
        return pd.DataFrame([dict])

    def outlog(self,text1="",text2="",text3=""):
        currentDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(text1,text2,text3)
        fo = open("log.txt", "a")
        logs=""
        # logs="========================="+currentDate +"=========================\n"
        logs+=text1+text2+text3 +"\n"
        fo  .writelines(logs)
        fo.close()



# codelist="sz000000"
# for k in range(100,888):
#     codelist+=",sz000"+str(k)
#     # print(k,"sz000"+str(k))
# # print(codelist)
# df=sn.GetSinaALLData(codelist)
# df=sn.GetSinaALLData("SZ000519,SZ000518,SZ000517,SZ000516,SZ000515,SZ000514,SZ000513")
# 日期        时间  状态  股票名称     开盘价    昨日收盘    当前价格    最高价格    最低价格     买入价     卖出价      成交数量            成交金额
# print("//////////////////////////////////////","df//////////////////////////////////////")
# print(df)
# print(df[["日期","时间","股票名称","开盘价","昨日收盘","当前价格","最高价格","最低价格","成交数量","成交金额"]])

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    printinfo("program is running....")

    sn = SinaData()
    sn.get_data()




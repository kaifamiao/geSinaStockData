#-*-coding:gb2312-*-
from colorama import init, Fore, Back, Style
init(autoreset=True)
def printinfo(text,colr="GREEN"):
    if colr=="CYAN":
        print(Fore.CYAN +Style.BRIGHT+ text)
    if colr=="RED":
        print(Fore.RED +Style.BRIGHT+ text)
    if colr=="BLUE":
        print(Fore.BLUE +Style.BRIGHT+ text)
    if colr=="GREEN":
        print(Fore.GREEN +Style.BRIGHT+ text)
    if colr=="WHITE":
        print(Fore.WHITE +Style.BRIGHT+ text)
    if colr=="YELLOW":
        print(Fore.YELLOW +Style.BRIGHT+ text)
    if colr=="MAGENTA":
        print(Fore.MAGENTA +Style.BRIGHT+ text)
    if colr=="LIGHTYELLOW_EX":
        print(Fore.LIGHTYELLOW_EX +Style.BRIGHT+ text)
    if colr=="REDB":
        print(Fore.RESET +Style.BRIGHT+Back.RED+ text)
    if colr=="MAGENTAB":
        print(Fore.RESET +Style.BRIGHT+Back.MAGENTA+ text)
    if colr=="BLUEB":
        print(Fore.WHITE +Style.BRIGHT+Back.BLUE+ text)
    if colr=="GREENB":
        print(Fore.YELLOW +Style.BRIGHT+Back.GREEN+ text)

def set_title():
    fo = open("banner.txt", "r")
    # print("文件名为: ", fo.name)
    strtmp = ""
    for line in fo.readlines():  # 依次读取每行
        # line = line.strip()  # 去掉每行头尾空白
        # print("读取的数据为: %s" % (line))
        strtmp += line

    # 关闭文件
    fo.close()
    return strtmp
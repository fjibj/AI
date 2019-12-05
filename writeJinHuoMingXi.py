# coding:utf-8
import datetime
import re
from urllib import request, parse
import math
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# 得到金字对应的陈列盘位置
def getJinPosition(hz):
    s = parse.quote(hz)
    url = 'http://www.zizaicn.com/weixin/xixifu_zzping_search_word.php?str=' + s
    f = request.urlopen(url)
    h = f.read().decode('utf-8')
    #print(h)
    m = re.search(r'查询结果：</strong><br>(.*):第(.*)行 (.*)列</div>', h)
    if m:
        return int(m.group(2)), int(m.group(3))
    else:
        return 1000, 1000


# 得到铅字对应的陈列盘位置
def getposition(hz):
    s = parse.quote(hz)
    url = 'http://www.zizaicn.com/weixin/getwordpos_ver2.php?str=' + s
    f = request.urlopen(url)
    h = f.read().decode('utf-8')
    m = re.search(r'查询结果：</strong><br>(.*)<br></div>', h)
    m2 = re.match(r'(.*):(.*)盘 (.*)行 (.*)列', m.group(1))
    if m2:
        return int(m2.group(2)), int(m2.group(3)), int(m2.group(4))
    else:
        return 1000, 1000, 1000


# 读金字.csv文件生成DataFrame
def sortJinPosition(csvfile):
    s = datetime.datetime.now()
    df = pd.read_csv(csvfile, header=None, names=['A', 'B'])
    # print(df['A'])
    df[['C', 'D']] = df.apply(lambda row: pd.Series(getJinPosition(row['A'])), axis=1)
    # print(df)
    # df.to_csv('sort1.csv', encoding='utf-8')
    df2 = df.sort_values(['C', 'D'], ascending=[True, True])
    df2.reset_index(drop=True, inplace=True)
    df2.to_csv('sort2.csv', encoding='utf-8')
    e = datetime.datetime.now()
    print('sort spended ' + str((e - s).seconds) + ' seconds.')
    return df2

# 读铅字.csv文件生成DataFrame
def sortposition(csvfile):
    s = datetime.datetime.now()
    df = pd.read_csv(csvfile, header=None, names=['A', 'B'])
    # print(df['A'])
    df[['C', 'D', 'E']] = df.apply(lambda row: pd.Series(getposition(row['A'])), axis=1)
    # print(df)
    # df.to_csv('sort1.csv', encoding='utf-8')
    df2 = df.sort_values(['C', 'D', 'E'], ascending=[True, True, True])
    df2.reset_index(drop=True, inplace=True)
    df2.to_csv('sort2.csv', encoding='utf-8')
    e = datetime.datetime.now()
    print('sort spended ' + str((e - s).seconds) + ' seconds.')
    return df2


# 获得在Excel文档中的行列位置(行，列，页）注：页表示对应的标签名称最后的()中的数字，如果为1，则标签名称不含()
# index：在df中的序号
# sc：起始列
# ine：列间隔
# ec: 终止列（数字列）
# sl：起始行
# el：终止行
def getxlspos(index, sc, ine, ec, sl, el):
    row = index % (el - sl + 1) + sl
    col = chr(ord(sc) + (index // (el - sl + 1)) * ine % (ord(ec)-ord(sc)+1))
    page = 1 + (index // ((ord(ec)-ord(sc)+1)*(el-sl+1)//ine))
    return col, row, page


# 写入《南京科举博物馆进货明细》铅字补字表（多标签页）
# df: 输入的包含'A''B'两列的DataFrame
# f：要写入的EXCEL文件
# la：要写入的EXCEL文件的标签页
# sc：起始列
# ine：列间隔
# ec: 终止列（数字列）
# sl：起始行
# el：终止行

def writein(df, f, la, sc, ine, ec, sl, el):
    wb = load_workbook(f)
    #ws = wb[la]
    i = 1 #标签页()内的数字，如：铅（金）字补字表 (2)
    for row in df.itertuples():
        # print(row[0], row[1], row[2])
        c, r, p = getxlspos(int(row[0]), sc, ine, ec, sl, el)
        print(c,r,p)
        ws = wb[la+' ('+str(p)+')' if p>1 else la]
        ws[c + str(r)].value = row[1]
        ws[chr(ord(c) + 1) + str(r)].value = int(row[2])
        if int(row[3]) == 1000:
            # 3-设置样式，并且加载到对应单元格
            fill = PatternFill("solid", fgColor="EE7AE9")
            ws[c + str(r)].fill = fill
    wb.save(f)


# 对EXCEL表格中的数值进行整除
# f：要写入的EXCEL文件
# la：要写入的EXCEL文件的标签页
# sc：起始列
# ine：列间隔
# ec: 终止列（数字列）
# sl：起始行
# el：终止行
# d: 整除数（如2，3）
def divide(f, la, sc, ine, ec, sl, el):
    wb = load_workbook(f)
    ws = wb[la]
    for c in range(ord(sc),ord(ec)+1,ine):
        col = chr(c)
        for row in range(sl,el+1):
            val = ws[col+str(row)].value
            if val:
                ws[col+str(row)].value = math.ceil(val/2)
                print(la, col+str(row), val, ws[col+str(row)].value)
    wb.save(f)

#df = sortposition('./11月补铅字.txt')
#print(getxlspos(47, 'A', 2, 7, 100))
#writein(df, './南京科举博物馆进货明细11.1.xlsx', '铅字补字表', 'A', 2, 7, 100)
#铅字补字表 (2)
#print(getxlspos(1395, 'A', 2, 'N', 7, 99))
s = datetime.datetime.now()
#writein(sortposition('./12月待补铅字.txt'), '../字在进货/2019.12月进货/南京科举博物馆进货明细12.3.xlsx', '铅字补字表', 'A', 2, 'N', 7, 99)
#divide('南京科举博物馆进货明细12.3.xlsx','金字补字表','B',3,'L',7,44)
#divide('南京科举博物馆进货明细12.3.xlsx','金字补字表 (2)','B',3,'H',7,44)
#divide('南京科举博物馆进货明细12.3.xlsx','铅字补字表','B',2,'N',7,99)
#divide('南京科举博物馆进货明细12.3.xlsx','铅字补字表 (2)','B',2,'N',7,99)
#divide('南京科举博物馆进货明细12.3.xlsx','铅字补字表 (3)','B',2,'D',7,99)
#print(sortJinPosition('12月待补金字.txt'))
writein(sortJinPosition('12月待补金字.txt'), '南京科举博物馆进货明细12.3.xlsx', '金字补字表', 'A', 3, 'L', 7, 44)

e = datetime.datetime.now()
print('All spended ' + str((e - s).seconds) + ' seconds.')
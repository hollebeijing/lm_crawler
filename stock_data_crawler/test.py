#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/14 上午11:48
    Author  : Richard Chen
    File    : test.py
    Software: IntelliJ IDEA
'''
import requests, json
from conf.requests_useragent import get_user_agent
from bs4 import BeautifulSoup
#
# headers = {
#     'Accept': '*/*',
#     'Connection': 'keep-alive',
#     'Referer': 'http://www.sse.com.cn/market/sseindex/diclosure/c/c_20151130_4017237.shtml',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'User-Agent': get_user_agent()
# }
#
#
# data = requests.get(
#     url='http://query.sse.com.cn/search/getSearchResult.do?search=qwjs&perpage=100&orderby=-CRELEASETIME&searchword=调整样本股&_=1513307156579',
#     headers=headers)
# data_dict = json.loads(data.text)
# for item in data_dict['data']:
#     print(item)

# fp = open('1.xlsx','wb')
# fp.write(data.content) #写入图片
# fp.close()

#
# first_2013 = '/aboutus/mediacenter/hotandd/c/c_20150912_3987651.shtml'
# second_2013 = '/market/sseindex/diclosure/c/c_20150911_3985098.shtml'
# first_2014 = '/market/sseindex/diclosure/c/c_20150911_3985111.shtml'
# second_2014 = '/market/sseindex/diclosure/c/c_20150911_3985128.shtml'
# first_2015 = '/market/sseindex/diclosure/c/c_20150911_3985155.shtml'
# second_2015 = '/market/sseindex/diclosure/c/c_20151130_4017237.shtml'
# first_2016 = '/market/sseindex/diclosure/c/c_20160530_4121664.shtml'
# second_2016 = '/market/sseindex/diclosure/c/c_20161128_4207421.shtml'
# first_2017 = '/market/sseindex/diclosure/c/c_20170531_4318582.shtml'
# second_2017 = '/market/sseindex/diclosure/c/c_20171127_4424760.shtml'

# import xlsxwriter
#
# value = {u'600000': [["名称", "价格", "出版社", "语言"],
#                      ["如何高效读懂一本书", "22.3", "机械工业出版社", "中文"],
#                      ["暗时间", "32.4", "人民邮电出版社", "中文"],
#                      ["拆掉思维里的墙", "26.7", "机械工业出版社", "中文"]],
#          u'600001': [["名称", "价格", "出版社", "语言"],
#                      ["如何高效读懂一本书", "22.3", "机械工业出版社", "中文"],
#                      ["暗时间", "32.4", "人民邮电出版社", "中文"],
#                      ["拆掉思维里的墙", "26.7", "机械工业出版社", "中文"]],
#          }
#
# workbook = xlsxwriter.Workbook('hello.xlsx')  # 建立文件
# for k, v in value.items():
#     worksheet = workbook.add_worksheet(k)
#     for i in range(0, len(v)):
#         for j in range(0, len(v[i])):
#             worksheet.write(i, j, str(v[i][j]))
#
# workbook.close()


import tushare as ts

import ssl

# ts.set_token('253e4d6798c327afc247b4322d521069803bab6c59aeeea6a97c40a5791f05ab')
# # ssl._create_default_https_context = ssl._create_unverified_context
# fd = ts.Idx()
# df = fd.IdxCons(ticker='000001', field='secShortName,consTickerSymbol,consShortName,isNew,intoDate')
# print(df)
# fd = ts.Idx()
# df = fd.IdxCons(ticker='000001', field='secShortName,consTickerSymbol,consShortName,isNew,intoDate')

# import requests
# url = 'https://api.wmcloud.com/data/v1//api/idx/getIdxConsECCXE.json?field=&secID=&ticker=000001&isNew='
# data  = requests.get(url)
# print(data.text)


# url_list = []
# from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
# import requests
# def tast(url):
#     print(requests.get(url).text)
# pool = ThreadPoolExecutor(10) #线程
# # pool = ProcessPoolExecutor(10) #进程
# for url in url_list:
#     pool.submit(tast,url)#线程池中获取一个线程，执行task函数
# pool.shutdown(wait=True)  #上面的线程池的任务都执行完了再往下走。


# data_list = [{'date': '2017-09-04', 'totalShares': '2935208.0397'},
#              {'date': '2017-05-26', 'totalShares': '2810376.3899'},
#              {'date': '2017-05-25', 'totalShares': '2161827.9922'},
#              {'date': '2017-03-20', 'totalShares': '2161827.9922'},
#              {'date': '2016-06-30', 'totalShares': '2161827.9922'},
#              {'date': '2016-06-24', 'totalShares': '2161827.9922'},
#              {'date': '2016-06-23', 'totalShares': '1965298.1747'},
#              {'date': '2016-03-18', 'totalShares': '1965298.1747'},
#              {'date': '2015-10-14', 'totalShares': '1865347.1415'},
#              {'date': '2011-06-07', 'totalShares': '1865347.1415'},
#              {'date': '2010-10-14', 'totalShares': '1434882.4165'},
#              {'date': '2010-09-29', 'totalShares': '1147905.9332'},
#              {'date': '2000-01-12', 'totalShares': '241000'}]

# d = [('', '2017-09-04'), ('2017-09-04', '2017-05-26'), ('2017-05-26', '2017-05-25'), ('2017-05-25', '2017-03-20'),
#      '''....''']
#
# # dd = [(data_list[i]['date'], data_list[i - 1]['date']) for i in range(1, len(data_list) + 1)]d
# dd = [("" if i == 0 else data_list[i - 1]["date"], "" if i == (len(data_list) -1) else data_list[i]["date"]) for i in
#       range(len(data_list))]
#
# cc = [("" if i == 0 else data_list[i-1]["date"], "" if i == (len(data_list)) else data_list[i]["date"],data_list[i]['totalShares']) for i in range(len(data_list))]
# # print(dd)
# print(cc)





import requests, json
from bs4 import BeautifulSoup
# # d = [(data_list[i]['date'],data_list[i-1]['date']) for i in range(len(data_list) +1)]
# url = 'http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?style=tail&id=6000001&num=1'
# # url = 'http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?dtype=25&style=tail&check=st&dtformat=HH:mm:ss&id=6000001&num=9'
#
# res = requests.get(url)
# res.encoding = 'utf-8'
# data_json = json.loads(res.text.split('(')[1].split(')')[0])
# print(data_json)
# if not data_json['result']:
#     if data_json['message'] =='暂无数据':
#         print('...')
#     else:
#         print('未找到股票代码')
# else:
#     print('未停牌')

# import requests
#
# res = requests.get(url='http://www.cninfo.com.cn/finalpage/2009-10-12/57126646.PDF')
# print(res.content)


# from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
#
# new_code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600019",
#                  "600104", "600111", "600340", "600309", "600518", "600519", "600547", "600606", "600837",
#                  "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
#                  "601669", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
#                  "601601", "601628", "601668", "601688", "601766", "601878", "601800", "601818", "601857",
#                  "601881", "603993", "601985", "601988", "601989"]
#
# for i in new_code_list:
#     data = LmInnerReportDBMgr.get_code_data('lm_stock_data', i)
#     if float(data['history_capital_stock'][0]['totalShares']) != float( data['sina_history_capital_stock'][-1]['totalShares']):
#         print(i,data['history_capital_stock'][0],data['sina_history_capital_stock'][-1])

# import rqalpha
# import tushare as ts
# import ssl
#
# ssl._create_default_https_context = ssl._create_unverified_context
# ts.set_token('d361de56f51ed98f28b4a4b8ebd7b1dd44ba97255cc780d5ee8deacbc2ef3831')
# fd = ts.Idx()
# df = fd.IdxCons(ticker='000016', field='secShortName,consTickerSymbol,consShortName,isNew,intoDate')
# print(df)
# from selenium import webdriver
# import time
# import requests

# browser = webdriver.Firefox()
# browser.get('https://www.joinquant.com/user/login/index')
# input_list = browser.find_element_by_class_name('kkform').find_elements_by_class_name('form-control')
# input_list[0].send_keys('17600185660')
# input_list[1].send_keys('Cx1994814')
# submit = browser.find_element_by_id('btnSubmit')
# submit.click()
# print(browser.get_cookies()[-1])
#
# res = requests.get(
#     url='https://www.joinquant.com/research?target=research&url=/user/71400787116/notebooks/Untitled.ipynb',
#     cookies=browser.get_cookies()[-1]
# )
# print(res)
# # browser.get('https://www.joinquant.com/research')
# browser.get('https://www.joinquant.com/research?target=research&url=/user/71400787116/notebooks/Untitled.ipynb')
# time.sleep(5)
# browser.get('https://www.joinquant.com/research?target=research&url=/user/71400787116/notebooks/Untitled.ipynb')
# a_list = browser.find_elements_by_class_name('item_link')
# # a_list[0].click()
# time.sleep(10)
# print(browser.page_source)
#
# print('========')
# print(browser.get_cookies())


# browser.find_element_by_class_name('kkform').find_elements_by_class_name('')
import json
from common.utils.time_utils import getEveryDay
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr

c_0405 = getEveryDay('2004-01-02', '2005-12-31', 1)  # 第一次获取
c_0607 = getEveryDay('2006-01-01', '2007-12-31', 1)  # 第二次获取
c_0809 = getEveryDay('2008-01-01', '2009-12-31', 1)  # 第二次获取
c_1011 = getEveryDay('2010-01-01', '2011-12-31', 1)  # 第二次获取
c_1213 = getEveryDay('2012-01-01', '2013-12-31', 1)  # 第二次获取
c_1415 = getEveryDay('2014-01-01', '2015-12-31', 1)
c_1617 = getEveryDay('2016-01-01', '2017-12-31', 1)  # 第二次获取

dlist = []
with open('0405', encoding='utf-8') as json_file:
    for i in json_file:
        d_0405 = eval(i)
for i in zip(c_0405, d_0405):
    if len(i[1]) != 50 :
        i[1].append('600018.XSHG')
    dlist.append({'date': i[0], 'cfg': i[1]})

with open('0607', encoding='utf-8') as json_file:
    for i in json_file:
        d_0607 = eval(i)
for i in zip(c_0607, d_0607):
    if len(i[1]) != 50 :
        i[1].append('600018.XSHG')
    dlist.append({'date': i[0], 'cfg': i[1]})

with open('0809', encoding='utf-8') as json_file:
    for i in json_file:
        d_0809 = eval(i)
dlist += [{'date': i[0], 'cfg': i[1]} for i in zip(c_0809, d_0809)]

with open('1011', encoding='utf-8') as json_file:
    for i in json_file:
        d_1011 = eval(i)
dlist += [{'date': i[0], 'cfg': i[1]} for i in zip(c_1011, d_1011)]

with open('1213', encoding='utf-8') as json_file:
    for i in json_file:
        d_1213 = eval(i)
dlist += [{'date': i[0], 'cfg': i[1]} for i in zip(c_1213, d_1213)]

with open('1415', encoding='utf-8') as json_file:
    for i in json_file:
        d_1415 = eval(i)
dlist += [{'date': i[0], 'cfg': i[1]} for i in zip(c_1415, d_1415)]

with open('1617', encoding='utf-8') as json_file:
    for i in json_file:
        d_1617 = eval(i)
dlist += [{'date': i[0], 'cfg': i[1]} for i in zip(c_1617, d_1617)]

LmInnerReportDBMgr.save_set_result('lm_index_data', {'code': '000016'}, 'constituent_shares_list', dlist)
# 第一次循环存储，库里没有数据的情况下
# for i in range(len(data)):
#     if i == 0:
#         data[0][1].append('600018.XSHG')
#         d_list.append({'date': data[0][0], 'cfg': data[0][1]})
#     else:
#         t = 0
#         for f in d_list[-1]['cfg']:
#             for s in data[i][1]:
#                 if f == s:
#                     t += 1
#         if t != 49:
#             data[i][1].append('600018.XSHG')
#             d_list.append({'date': data[i][0], 'cfg': data[i][1]})
# LmInnerReportDBMgr.save_set_result('lm_index_data', {'code': '000016'}, 'constituent_shares_list', d_list)
# 第二次存储，库里有数据，按照库里最后一个日期的数据对比
# mong_data = LmInnerReportDBMgr.get_data('lm_index_data', {'code': '000016'})['constituent_shares_list']
# tag = True
# for i in data:
#     if tag:
#         t = 0
#         if '600018.XSHG' not in i[1]:
#             i[1].append('600018.XSHG')
#         for f in mong_data[-1]['cfg']:
#             for s in i[1]:
#                 if f == s:
#                     t += 1
#         if t != 50:
#             d_list.append({'date': i[0], 'cfg': i[1]})
#             tag = False
#     else:
#         t = 0
#
#         if '600018.XSHG' not in i[1]:
#             i[1].append('600018.XSHG')
#         for f in d_list[-1]['cfg']:
#             for s in i[1]:
#                 if f == s:
#                     t += 1
#         if t != 50:
#             d_list.append({'date': i[0], 'cfg': i[1]})
#             tag = False
# mong_data += d_list

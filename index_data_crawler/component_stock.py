#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/20 下午3:17
    Author  : Richard Chen
    File    : component_stock.py
    Software: IntelliJ IDEA
'''
import requests, json
from conf.requests_useragent import get_user_agent
from bs4 import BeautifulSoup
from common.utils.time_utils import get_date_object
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
import re
import traceback

headers = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Referer': 'http://www.sse.com.cn/market/sseindex/diclosure/c/c_20151130_4017237.shtml',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'User-Agent': get_user_agent()
}

baes_url = 'http://www.sse.com.cn'
import xlrd
from collections import defaultdict
import re


def entry_into_force_time(url):
    '''
    获取生效时间
    :param url:
    :return: str 2016-01-10
    '''
    first_res = requests.get(url=baes_url + url, headers=headers)
    first_res.encoding = 'utf-8'
    soup = BeautifulSoup(first_res.text, 'lxml')
    date_y = get_date_object(str(soup.find('div', class_='article_opt').find('i').text).strip()).year
    p_list = soup.find('div', class_='allZoom').find_all('p')
    take_effect_text = re.findall(r'(\w+月\w+日正式生效)', p_list[0].text)
    if take_effect_text:
        date_m_d = re.findall(r'([0-9]+)', take_effect_text[0])
        if len(date_m_d) == 2:
            com_date = '%s%s%s' % (date_y, date_m_d[0], date_m_d[1])
        else:
            com_date = '%s%s%s' % (date_m_d[0], date_m_d[1], date_m_d[2])
    else:
        take_effect_text = re.findall(r'(\w+月\w+日正式生效)', p_list[1].text)
        if take_effect_text:
            date_m_d = re.findall(r'([0-9]+)', take_effect_text[0])
            if len(date_m_d) == 2:
                com_date = '%s%s%s' % (date_y, date_m_d[0], date_m_d[1])
            else:
                com_date = '%s%s%s' % (date_m_d[0], date_m_d[1], date_m_d[2])
        else:
            take_effect_text = re.findall(r'(\w+月\w+日正式生效)', p_list[-1].text)
            if not take_effect_text:
                print('请查看具体页面:%s' % url)
            date_m_d = re.findall(r'([0-9]+)', take_effect_text[0])
            if len(date_m_d) == 2:
                com_date = '%s%s%s' % (date_y, date_m_d[0], date_m_d[1])
            else:
                com_date = '%s%s%s' % (date_m_d[0], date_m_d[1], date_m_d[2])
    com_date = get_date_object(com_date, "%Y%m%d").date()
    return com_date


def add_component_code(wb, data, type):
    '''
    处理调入code代码
    :param wb: 打开文件的对象
    :param data: 现有数据库成分股
    :param type: 0:将数据库成分股中删除调入的code，1:将调入的code添加到现有数据库成分的数据中
    :return: 添加或删除后的list
    '''
    tr_d = wb.sheets()[0]
    indexs_list = defaultdict(list)
    for k, va in [(v, i) for i, v in enumerate(tr_d.col_values(0))]:
        indexs_list[k].append(va)
    tr_code = []
    for index in indexs_list['000016']:
        tr_code.append({'code': tr_d.row_values(index)[2], 'name': tr_d.row_values(index)[3]})
    if type:
        data += tr_code
    else:
        for code in tr_code:
            print(code)
            data.remove(code)
    return data


def out_component_code(wb, data, type):
    '''
    处理调出code代码
    :param wb: 打开文件的对象
    :param data: 现有数据库成分股
    :param type: 0:将数据库成分股中删除调出的code，1:将调出的code添加到现有数据库成分的数据中
    :return: 添加或删除后的list
    '''
    tc_d = wb.sheets()[1]
    indexs_list = defaultdict(list)
    for k, va in [(v, i) for i, v in enumerate(tc_d.col_values(0))]:
        indexs_list[k].append(va)
    tc_code = []
    for index in indexs_list['000016']:
        tc_code.append({'code': tc_d.row_values(index)[2], 'name': tc_d.row_values(index)[3]})
    if type:
        data += tc_code
    else:
        for code in tc_code:
            data.remove(code)
    return data


def obtain_xlsx_data(url):
    res = requests.get(url=baes_url + url, headers=headers, timeout=15)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    p_list = soup.find('div', class_='allZoom').find_all('p')
    a_list = p_list[-1].find_all('a')
    if a_list:
        adjust_xlsx_url = a_list[-1].get('href')
    else:
        a_list = p_list[-2].find_all('a')
        adjust_xlsx_url = a_list[-1].get('href')
    xlsx_data = requests.get(url=baes_url + adjust_xlsx_url, headers=headers)
    xlsx_data.encoding = 'utf-8'
    with open('tmp.xlsx', 'wb') as f:
        for chunk in xlsx_data:
            f.write(chunk)
        f.close()


def func():
    first_2013 = '/aboutus/mediacenter/hotandd/c/c_20150912_3987651.shtml'
    second_2013 = '/market/sseindex/diclosure/c/c_20150911_3985098.shtml'
    first_2014 = '/market/sseindex/diclosure/c/c_20150911_3985111.shtml'
    second_2014 = '/market/sseindex/diclosure/c/c_20150911_3985128.shtml'
    first_2015 = '/market/sseindex/diclosure/c/c_20150911_3985155.shtml'
    second_2015 = '/market/sseindex/diclosure/c/c_20151130_4017237.shtml'
    first_2016 = '/market/sseindex/diclosure/c/c_20160530_4121664.shtml'
    second_2016 = '/market/sseindex/diclosure/c/c_20161128_4207421.shtml'
    first_2017 = '/market/sseindex/diclosure/c/c_20170531_4318582.shtml'
    second_2017 = '/market/sseindex/diclosure/c/c_20171127_4424760.shtml'
    url_list = [second_2017, first_2017]
    try:
        for i in range(len(url_list)):
            obtain_xlsx_data(url_list[i])
            shxx_date = entry_into_force_time(url_list[i -1])
            # 获取列表中最后一个日期
            mongo_save_date = \
                list(LmInnerReportDBMgr.get_index_comstock_data('lm_index_data', {'code': '000016'}).keys())[-1]
            data_list = LmInnerReportDBMgr.get_index_comstock_teble('lm_index_data', {'code': '000016'},
                                                                '2014-06-16')

            print(data_list)
            wb = xlrd.open_workbook('20131216.xls')
            #将调入的调出去，调出的调进来(往前推理成分股)
            tr_data = add_component_code(wb, data_list, 0)
            tc_data = out_component_code(wb, tr_data, 1)
            # #将调入的调进去，调出的调出去(往后推理成分股)
            # tr_data = add_component_code(wb, data_list, 1)
            # tc_data = out_component_code(wb, tr_data, 0)

            LmInnerReportDBMgr.save_set_result('lm_index_data', {'code': '000016'},
                                               'component_stock_dict.%s' % '2013-12-16',
                                               tc_data)
    except Exception as e:
        traceback.print_exc(e)


if __name__ == '__main__':
    func()

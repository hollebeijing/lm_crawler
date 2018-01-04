#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/2 下午8:26
    Author  : Richard Chen
    File    : capital_data.py
    Software: IntelliJ IDEA
'''
import requests
from bs4 import BeautifulSoup
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from conf.requests_useragent import get_user_agent
from common.utils.time_utils import date_timestamp


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': get_user_agent(),
}
def history_sina_capital(code):
    res = requests.get(
        url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/{}/stocktype/TotalStock.phtml'.format(code),
        headers=headers,
    )
    res.encoding = 'gb2312'
    soup = BeautifulSoup(res.text, 'lxml')
    tr_list = soup.find('table', id='StockStructureHistoryTable').find_all('tr')[2].find('table').find_all(
        id=['historyTable07', 'historyTable06', 'historyTable05'])
    data_list = []
    for tr in tr_list:
        for item in tr.find_all('tr'):
            if item.find_all('td'):
                data_list.append({'date': item.find_all('td')[0].text,
                                  'totalShares': str(item.find_all('td')[1].text).replace('万股', '')})
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': code}, 'sina_history_capital_stock', data_list)

    print(code, 'sina_history_capital_stock finish...')



def daily_sina_capital(code):
    res = requests.get(
        url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/{}/stocktype/TotalStock.phtml'.format(code),
        headers=headers,
    )
    res.encoding = 'gb2312'
    soup = BeautifulSoup(res.text, 'lxml')
    tr_list = soup.find('table', id='StockStructureHistoryTable').find_all('tr')[2].find('table').find_all(
        id=['historyTable07', 'historyTable06', 'historyTable05'])
    data_list = []
    for tr in tr_list:
        for item in tr.find_all('tr'):
            if item.find_all('td'):
                data_list.append({'date': item.find_all('td')[0].text,
                                  'totalShares': str(item.find_all('td')[1].text).replace('万股', '')})
    wz_date = date_timestamp(data_list[-1]['date'])
    db_date = date_timestamp(LmInnerReportDBMgr.get_data_list('lm_stock_data',{'code': code},'sina_history_capital_stock')[-1]['date'])
    if wz_date >db_date:
        print(code,'有变更股本信息,变更前日期为:%s,变更后日期为:%s')
        LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': code}, 'sina_history_capital_stock', data_list)
    else:
        print(code,'股本信息已经是最新...')


if __name__ == '__main__':
    pass
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/27 下午12:53
    Author  : Richard Chen
    File    : sina.py
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
            # table_list = soup.find('div', id='con02-1').find_all('table')
            # all_data = []
            # for table in table_list:
            #     tr_list = table.find('tbody').find_all('tr')
            #     date = [tr_list[0].find_all('td')[i].text for i in range(1, len(tr_list[0].find_all('td')))]
            #     changeReasonDesc = [tr_list[3].find_all('td')[i].text for i in range(1, len(tr_list[3].find_all('td')))]
            #     totalShares = [str(tr_list[4].find_all('td')[i].text).split(' ')[0] for i in
            #                    range(1, len(tr_list[4].find_all('td')))]
            #     all_data += zip(date, totalShares, changeReasonDesc)
            # data_dict = [{'date': i[0], 'totalShares': i[1], 'changeReasonDesc': i[2]} for i in all_data]


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
    # sina_capital('1')
    code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600100",
                 "600104", "600111", "600340", "600485", "600518", "600519", "600547", "600606", "600837",
                 "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
                 "601198", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
                 "601601", "601628", "601668", "601688", "601766", "601788", "601800", "601818", "601857",
                 "601881", "601901", "601985", "601988", "601989",'600019', '600309', '601669', '601878', '603993']
    # code_list = ['600000']

    for code in code_list:
        daily_sina_capital(code)
        # time.sleep(10)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/2 下午8:34
    Author  : Richard Chen
    File    : price_data.py
    Software: IntelliJ IDEA
'''

import requests
import json
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from conf.requests_useragent import get_user_agent
from data_crawler.Eastmoney.history_data_crawler.price_data import is_halt


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': get_user_agent(),
}

def Tencent_history_price_crawler(code):
    url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh{},day,2002-01-01,2010-01-31,320,qfq'.format(code)
    res = requests.get(
        url=url,
        headers=headers,
    )
    stock_data = json.loads(res.text)['data']['sh600591']['qfqday']
    stock_name = json.loads(res.text)['data']['sh600591']['qt']['sh600591'][1]
    isHalt = is_halt(code)
    all_day_data_list = []
    for day_data in stock_data:  # ['2008-07-15', '6.100', '6.070', '6.240', '6.000', '133681.350'] [date,开盘价,收盘价,最高价,最低价,交易量]
        day_date = day_data[0]
        opening = day_data[1]
        settlement = day_data[2]
        ceilingPrice = day_data[3]
        bottomPrice = day_data[4]
        volumeOfTransaction = day_data[5]
        all_day_data_list.append({
            'date': day_date,
            'opening': opening,
            'settlement': settlement,
            'ceilingPrice': ceilingPrice,
            'bottomPrice': bottomPrice,
            'volumeOfTransaction': volumeOfTransaction,
        })
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': code}, 'history_price_stock',
                                       all_day_data_list)
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': code}, 'company_name', stock_name)
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': code}, 'isHalt', isHalt)
    print('%s save history price of stock successful...' % stock_name)

class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    pass
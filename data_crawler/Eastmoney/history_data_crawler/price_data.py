#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/2 下午8:31
    Author  : Richard Chen
    File    : price_data.py
    Software: IntelliJ IDEA
'''
import requests
import json
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from conf.requests_useragent import get_user_agent

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': get_user_agent(),
}


def is_halt(code):
    url = 'http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?style=tail&id={}1&num=1'.format(code)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    data_json = json.loads(res.text.split('(')[1].split(')')[0])
    if not data_json['result']:
        if data_json['message'] == '暂无数据':
            return 0
        else:
            print('未找到股票代码')
    else:
        return 1


def dfcf_history_price_crawler(code):
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id={}1&type=k'.format(code)
    data = requests.get(url=url, headers=headers)
    data_json = json.loads(data.text.split('(')[1].split(')')[0])
    stock_code = data_json['code']
    stock_name = data_json['name']
    stock_data = data_json['data']
    all_day_data_list = []
    isHalt = is_halt(code)
    for i in stock_data:  # i 就是一天的数据
        # [1999-11-10,29.50,27.75,29.80,27.00,1740850,48.6亿,-] [date,开盘价,收盘价,最高价,最低价,交易量,交易金额,振幅]
        day_data = str(i).split(',')
        day_date = day_data[0] #date
        opening = day_data[1] #开盘价
        settlement = day_data[2] #收盘价
        ceilingPrice = day_data[3] #最高价
        bottomPrice = day_data[4] #最低价
        volumeOfTransaction = day_data[5] #交易量
        # transactionAmount = day_data[6] #交易金额
        all_day_data_list.append({
            'date': day_date,
            'opening': opening,
            'settlement': settlement,
            'ceilingPrice': ceilingPrice,
            'bottomPrice': bottomPrice,
            'volumeOfTransaction': volumeOfTransaction,
            # 'transactionAmount': transactionAmount,
        })
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'history_price_stock',
                                       all_day_data_list)
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'company_name', stock_name)
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'isHalt', isHalt)
    print('%s save history price of stock successful...' % stock_name)


if __name__ == '__main__':
    pass
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/26 下午4:40
    Author  : Richard Chen
    File    : daily_share_capital.py
    Software: IntelliJ IDEA
'''
import requests, json
from common.utils import time_utils


def func():
    date_stamp = time_utils.date_timestamp('2017-12-01')

    url = 'http://emweb.securities.eastmoney.com/PC_HSF10/CapitalStockStructure/CapitalStockStructureAjax?code=sh601818'
    res = requests.get(url)
    res_data = json.loads(res.text)['Result']['ShareChangeList']
    capital_data = zip(res_data[0]['changeList'], res_data[1]['changeList'], res_data[-1]['changeList'])
    # print(capital_data)
    for i in capital_data:
        print(i)
    # for i in res_data[0]['changeList']:
    #     if time_utils.date_timestamp(i) > date_stamp:
    #         index_inster = res_data[0]['changeList'].index(i)
    #         print(res_data[0]['changeList'][index_inster])
    #         print(float(res_data[1]['changeList'][index_inster].replace(',', '')))
    #         print(res_data[-1]['changeList'][index_inster])


if __name__ == '__main__':
    func()

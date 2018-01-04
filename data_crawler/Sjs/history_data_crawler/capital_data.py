#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/2 下午8:18
    Author  : Richard Chen
    File    : capital_data.py
    Software: IntelliJ IDEA
'''
from conf.requests_useragent import get_user_agent
import requests,json
from common.db_utils.stock_crawler_inner_db import BaseCrawlerDB
from data_crawler.Excel.history_data_crawler.capital_data import capttal_xlsx_to_db
from data_crawler.Excel.write_excel import write07Excel


def install_history_capttal_crawler(code):
    '''
    爬去到数据后，直接根据stock_code,直接入库
    爬取上交所的股本信息，由于上交所更新过慢，则不用
    :return:
    '''
    capital_headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'keep-http://www.sse.com.cn/assortment/stock/list/info/capital/index.shtml',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': get_user_agent()
    }
    data_dicts = {}
    capital_url = 'http://query.sse.com.cn/security/stock/queryEquityChangeAndReason.do?companyCode={}'.format(code)
    data = requests.get(url=capital_url, headers=capital_headers)
    data_dict = json.loads(data.text)
    stock_code = data_dict['companyCode']
    history_capital_stock = data_dict['result']
    data_list = [['realDate', 'changeReasonDesc', 'totalShares'], ]
    for i in history_capital_stock:
        data_list.append(
            [i['realDate'], i['changeReasonDesc'], i['totalShares']])
    data_dicts[stock_code] = data_list
    # write07Excel(data_dicts)
    BaseCrawlerDB.save_set_result('lm_stock_data', {'code': stock_code}, 'history_capital_stock',
                                  history_capital_stock)
    capttal_xlsx_to_db(code)
    print('%s save history capital of stock successful...' % code)


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    pass
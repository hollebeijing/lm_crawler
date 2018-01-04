#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午4:54
    Author  : Richard Chen
    File    : history_capital_stock.py
    Software: IntelliJ IDEA
'''

import requests, json
from conf.requests_useragent import get_user_agent
from common.db_utils.stock_crawler_inner_db import BaseCrawlerDB


from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from common.utils import time_utils


def old_install_history_capttal_crawler(code):
    '''
    由于东方财富的股本只精确到小数点后两位。
    :param code:
    :return:
    '''
    url = 'http://emweb.securities.eastmoney.com/PC_HSF10/CapitalStockStructure/CapitalStockStructureAjax?code=sh601818'
    res = requests.get(url)
    res_data = json.loads(res.text)['Result']['ShareChangeList']
    capital_data = [{'date': item[0], 'totalShares': str(item[1]).replace(',', ''), 'changeReasonDesc': item[2]} for
                    item in zip(res_data[0]['changeList'], res_data[1]['changeList'], res_data[-1]['changeList'])]
    # capttal_xlsx_to_db(code, capital_data[-1]['date'], capital_data[-1]['totalShares'])



if __name__ == '__main__':
    install_history_capttal_crawler('600000')
    # install_history_capttal_crawler()
    # capttal_xlsx_to_db()

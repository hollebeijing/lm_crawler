#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午10:05
    Author  : Richard Chen
    File    : install_history_data.py
    Software: IntelliJ IDEA
'''

from json.decoder import JSONDecodeError

from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from data_handle.history_data.price_stock_of_capital import install_capital_to_price
from data_handle.history_data.total_market_value import total_market
# from stock_data_crawler.history_data.history_capital_stock import install_history_capttal_crawler
from index_data_crawler.sina import history_sina_capital
from stock_data_crawler.history_data.history_financial_stock import install_history_financial_crawler


def install():
    # code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600100",
    #                  "600104", "600111", "600340", "600485", "600518", "600519", "600547", "600606", "600837",
    #                  "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
    #                  "601198", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
    #                  "601601", "601628", "601668", "601688", "601766", "601788", "601800", "601818", "601857",
    #                  "601881", "601901", "601985", "601988", "601989",'600019', '600309', '601669', '601878', '603993']
    # code_list=['600000']
    code_list = []
    data = LmInnerReportDBMgr.get_data('lm_index_data', {'code': '000016'})['constituent_shares_list']
    for item in data:
        for code in item['cfg']:
            if str(code).split('.')[0] not in code_list:
                code_list.append(str(code).split('.')[0])
    print(len(code_list))
    print(code_list)
    code_list = code_list[55:]
    print(code_list)
    for code in code_list:
        try:
            install_history_financial_crawler(code)
            install_history_price_crawler(code)
            history_sina_capital(code)
            install_capital_to_price(code)
            total_market(code)
        except JSONDecodeError:
            continue


if __name__ == '__main__':
    install()

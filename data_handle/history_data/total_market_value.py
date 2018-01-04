#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/22 下午1:15
    Author  : Richard Chen
    File    : total_market_value.py
    Software: IntelliJ IDEA
'''

from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr


def total_market(code):
    code_data = LmInnerReportDBMgr.get_code_data('lm_stock_data', code)
    history_price_stock = code_data['history_price_stock']
    for item in history_price_stock:
        total_market = float(item['settlement']) * float(item['capital_stock'])
        item['total_market'] = total_market
    LmInnerReportDBMgr.save_set_result(tablename='lm_stock_data', condition={'code': code},
                                       result_type='history_price_stock', result=history_price_stock)
    print(code, 'total_market finish...')


if __name__ == '__main__':
    # code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600100",
    #              "600104", "600111", "600340", "600485", "600518", "600519", "600547", "600606", "600837",
    #              "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
    #              "601198", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
    #              "601601", "601628", "601668", "601688", "601766", "601788", "601800", "601818", "601857",
    #              "601881", "601901", "601985", "601988", "601989"]
    # code_list = ['600000']
    new_code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600019",
                     "600104", "600111", "600340", "600309", "600518", "600519", "600547", "600606", "600837",
                     "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
                     "601669", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
                     "601601", "601628", "601668", "601688", "601766", "601878", "601800", "601818", "601857",
                     "601881", "603993", "601985", "601988", "601989"]
    for code in new_code_list:
        total_market(code)

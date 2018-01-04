#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/14 下午1:58
    Author  : Richard Chen
    File    : price_stock_of_capital.py
    Software: IntelliJ IDEA
'''

from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from common.utils.time_utils import *


def install_capital_to_price(code):
    code_data = LmInnerReportDBMgr.get_code_data('lm_stock_data', code)
    if code_data:
        history_price_stock = code_data['history_price_stock']
        # history_capital_stock = code_data['history_capital_stock']
        history_capital_stock = code_data['sina_history_capital_stock']
        date_list = [("" if i == 0 else history_capital_stock[i - 1]["date"],
                      "" if i == (len(history_capital_stock)) else history_capital_stock[i]["date"],
                      history_capital_stock[i]['totalShares']) for i in
                     range(len(history_capital_stock))]
        for date_t in date_list:
            if date_t[0] == "":
                end_date = history_price_stock[-1]['date']
                begin_date = date_t[1]
                date_list = getEveryDay(begin_date, end_date, 1)
            else:
                end_date = date_t[0]
                begin_date = date_t[1]
                date_list = getEveryDay(begin_date, end_date, 0)
            for price in history_price_stock:
                for date in date_list:
                    if price['date'] == date:
                        price['capital_stock'] = date_t[2]
        install_capital_to_price_enddate(history_price_stock, history_capital_stock, code)
        print(code, 'price stock of capital finish....')


def install_capital_to_price_enddate(history_price_stock, history_capital_stock, code):
    begin_date = history_price_stock[0]['date']
    end_date = history_capital_stock[-1]['date']
    date_lists = getEveryDay(begin_date, end_date, 1)
    for price in history_price_stock:
        for date in date_lists:
            if price['date'] == date:
                price['capital_stock'] = history_capital_stock[-1]['totalShares']
    LmInnerReportDBMgr.save_set_result(tablename='lm_stock_data', condition={'code': code},
                                       result_type='history_price_stock', result=history_price_stock)


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
        install_capital_to_price(code)

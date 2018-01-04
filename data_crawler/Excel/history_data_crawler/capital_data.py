#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/2 下午8:22
    Author  : Richard Chen
    File    : capital_data.py
    Software: IntelliJ IDEA
'''
from datetime import datetime

from xlrd import xldate_as_tuple

from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from data_crawler.Excel.write_excel import read_xlsx


def capttal_xlsx_to_db(code):
    sheet = read_xlsx(code)
    data_list = []
    for i in range(sheet.nrows):
        if i == 0:
            continue
        d = {}
        for j in range(sheet.ncols):
            cell = sheet.cell_value(i, j)
            if sheet.cell(i, j).ctype == 3:
                date = datetime(*xldate_as_tuple(cell, 0))
                cell = date.strftime('%Y-%m-%d')
                if j == 0:
                    d['date'] = cell
                elif j == 1:
                    d['changeReasonDesc'] = cell
                else:
                    d['totalShares'] = cell
            else:
                # text格式
                if j == 0:
                    d['date'] = cell
                elif j == 1:
                    d['changeReasonDesc'] = cell
                else:
                    d['totalShares'] = cell
        data_list.append(d)
    LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': code}, 'history_capital_stock', data_list)


if __name__ == '__main__':
    pass
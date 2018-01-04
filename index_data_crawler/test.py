#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/20 下午4:12
    Author  : Richard Chen
    File    : test.py
    Software: IntelliJ IDEA
'''

import xlrd
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr

data = xlrd.open_workbook('000016cons.xls')
table = data.sheets()[0]
cols_code = table.col_values(0)
cols_name = table.col_values(1)
for i in range(1, len(cols_code)):
    LmInnerReportDBMgr.save_push_result('lm_index_data', {'code': '000016'}, 'component_stock_dict.20170612',
                                        {'code': cols_code[i], 'name': cols_name[i]})

if __name__ == '__main__':
    pass

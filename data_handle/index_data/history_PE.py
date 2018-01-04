#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/4 上午10:24
    Author  : Richard Chen
    File    : history_PE.py
    Software: IntelliJ IDEA
'''
'''
分析说明
    规则方法
        1: 当前年的前两个季度，和上一年的后两个季度
        2: 当前年的第一个季度，和上一年的后三个季度
        3: 时间排序，取最小时间的日期，取最小日期年份的前三个季度，和最小日期年份上一年的第四个季度
    第一步按照规则存储方法:
        third : [
            [最新日期到此年限或上一年的11-01(要判断最新日期月份是不是12月，如果是12月那么就是当前年份的11-01，如果是1月或2月或3月或4月，就用上一年份的11-01)]
            [最新日期此年的4月30到一下年的11-01日]
        ]
        second : [
            [每一年08-31到05-01]
        ]
        first :[
            [每一年的10-31到09-01]
        ]
    第二步
        按照每个列表日期进行规则处理
'''

from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from common.utils.time_utils import getEveryDay, get_date_object

date_dict = {
    'first': [],
    'second': [],
    'third': [],
}
constituent_shares_list = LmInnerReportDBMgr.get_data_list('lm_index_data', {'code': '000016'},
                                                           'constituent_shares_list')
__list = sorted(constituent_shares_list, key=lambda item: item['date'], reverse=True)

max_date = __list[0]['date']
min_date = __list[-1]['date']
# 1、获取此指数从头到尾的所有日期
date_list = getEveryDay(min_date, max_date, 1)
date_list = sorted(date_list, reverse=True)
# 2、将日期按照规则分配到date_dict中
for date in date_list:
    date_obj = get_date_object(date)
    # [每一年的10-31到09-01]
    if 9 <= date_obj.month <= 10:
        date_dict['first'].append(date)
    # [每一年08-31到05-01]
    elif 5 <= date_obj.month <= 8:
        date_dict['second'].append(date)
    # [最新日期到此年限或上一年的11-01(要判断最新日期月份是不是12月，如果是12月那么就是当前年份的11-01，如果是1月或2月或3月或4月，就用上一年份的11-01)]
    # [最新日期此年的4月30到一下年的11-01日]
    else:
        date_dict['third'].append(date)

print(date_dict['third'])
print(__list[0]['date'])
print(__list[0]['cfg'])
if __list[0]['date'] in date_dict['first']:
    print('当前年的前两个季度，和上一年的后两个季度')
elif __list[0]['date'] in date_dict['second']:
    print('当前年的第一个季度，和上一年的后三个季度')
else:
    date_obj = get_date_object(__list[0]['date'])
    date_month = date_obj.month
    date_year = date_obj.year
    print('如果当前月是12和11,如果当前月是1、2、3、4')
    if date_month in (11, 12):
        print('那么就用当前年后三个季度净利润和上一年最后一季度的净利润')
        #过去四个月净利润，和当前天的总市值  \][/p.k,j hbv
    elif date_month in (1, 2, 3, 4):
        print('那么就是用上一年的后三个季度，和上上年的最后一个季度')
    else:
        print('不在11，12，1，2，3，4中')

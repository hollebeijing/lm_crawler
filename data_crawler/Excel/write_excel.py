#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/15 下午10:19
    Author  : Richard Chen
    File    : write_excel.py
    Software: IntelliJ IDEA
'''
import xlsxwriter
import xlrd
import openpyxl


def write07Excel(data_dict):
    workbook = xlsxwriter.Workbook('sz_50_new.xlsx')  # 建立文件
    for k, v in data_dict.items():
        print(k,v)
        worksheet = workbook.add_worksheet(k)
        for i in range(0, len(v)):
            for j in range(0, len(v[i])):
                worksheet.write(i, j, str(v[i][j]))
    workbook.close()

def read_xlsx(sheet_name):
    workbook = xlrd.open_workbook('sz_50_2017_12_21.xlsx')
    sheet_data = workbook.sheet_by_name(sheet_name)
    return sheet_data


if __name__ == '__main__':
    from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
    # code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600100",
    #              "600104", "600111", "600340", "600485", "600518", "600519", "600547", "600606", "600837",
    #              "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
    #              "601198", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
    #              "601601", "601628", "601668", "601688", "601766", "601788", "601800", "601818", "601857",
    #              "601881", "601901", "601985", "601988", "601989"]
    code_list = ['600019', '600309', '601669', '601878', '603993']
    d_dict = {}
    for code in code_list :
        data_list = LmInnerReportDBMgr.get_code_data('lm_stock_data',code)
        total_market = data_list['history_price_stock'][-1]['total_market']
        d_dict[code] = total_market
    print(d_dict)
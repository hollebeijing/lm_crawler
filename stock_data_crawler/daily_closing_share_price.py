#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午7:53
    Author  : Richard Chen
    File    : daily_closing_share_price.py
    Software: IntelliJ IDEA
'''

import requests, json
from bs4 import BeautifulSoup
from conf.requests_useragent import get_user_agent
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from common.utils.time_utils import get_today_date, date_timestamp, timestamp_date


def testing_code(code):
    first_number = code[0]
    if first_number in ['0', '2', '3']:
        return '1' + code
    elif first_number in ['6', '9']:
        return '0' + code
    else:
        return ''


def install_daily_sharepirce(code):
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id={}1&type=k'.format(code)
    data = requests.get(url=url)
    data_json = json.loads(data.text.split('(')[1].split(')')[0])
    stock_data = data_json['data']
    # [1999-11-10,29.50,27.75,29.80,27.00,1740850,48.6亿,-] [date,开盘价,收盘价,最高价,最低价,交易量,交易金额,振幅]
    day_data = str(stock_data[-1]).split(',')
    day_date = day_data[0]
    opening = day_data[1]
    settlement = day_data[2]
    ceilingPrice = day_data[3]
    bottomPrice = day_data[4]
    volumeOfTransaction = day_data[5]
    transactionAmount = day_data[6]
    amplitude = day_data[7]
    today_date = date_timestamp(get_today_date())
    capital_data_list = LmInnerReportDBMgr.get_data_list('lm_stock_data', {'code': code}, 'sina_history_capital_stock')
    # capital_data_list = LmInnerReportDBMgr.get_data_list('lm_stock_data', {'code': code}, 'history_capital_stock')
    date_list = [date_timestamp(item['date']) for item in capital_data_list]
    sorted(date_list)
    print(date_list)
    max_date = date_list[-1]
    date = timestamp_date(max_date)
    if max_date == today_date:
        date = timestamp_date(date_list[-2])
    for item in capital_data_list:
        if item['date'] == date:

            capital_stock = item['totalShares']
            all_day_data = {
                'date': day_date,
                'opening': opening,
                'settlement': settlement,
                'ceilingPrice': ceilingPrice,
                'bottomPrice': bottomPrice,
                'volumeOfTransaction': volumeOfTransaction,
                'transactionAmount': transactionAmount,
                'amplitude': amplitude,
                'capital_stock': capital_stock,
                'total_market': float(settlement) * float(capital_stock)
            }
            LmInnerReportDBMgr.save_push_result('lm_stock_data', {'code': code}, 'history_price_stock', all_day_data)

            # LmInnerReportDBMgr.save_set_result('lm_index_data', {'code': stock_code}, 'history_price_stock', all_day_data_list)
            # LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'history_price_stock',
            #                                    all_day_data_list)
            # LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'company_name', stock_name)
            # print('%s save history price of stock successful...' % stock_name)
            # day_date = day_data[0]
            # opening = day_data[1]
            # settlement = day_data[2]
            # ceilingPrice = day_data[3]
            # bottomPrice = day_data[4]
            # volumeOfTransaction = day_data[5]
            # transactionAmount = day_data[6]
            # amplitude = day_data[7]
            # stock_daily_data = {
            #     'date': day_date,
            #     'opening': opening,
            #     'settlement': settlement,
            #     'ceilingPrice': ceilingPrice,
            #     'bottomPrice': bottomPrice,
            #     'volumeOfTransaction': volumeOfTransaction,
            #     'transactionAmount': transactionAmount,
            #     'amplitude': amplitude,
            # }

            # print(stock_daily_data)
            # srt_code = ''
            # for code in code_list:
            # srt_code += testing_code(code) + ','
            # url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id={}1&type=k'.format(code)
            # respones = requests.get(base_url.format(srt_code), headers=headers)
            # data_dict = json.loads(respones.text.split("(")[1].split(")")[0])
            # for code in code_list:
            #     try:
            #         c_code = testing_code(code)
            #         price = data_dict[c_code]['price']
            #         update_time = data_dict[c_code]['time']
            #         type = data_dict[c_code]['type']
            #         print(code, price, update_time, type)
            # response = requests.get(url=gb_url.format(i),
            #                         headers=headers)
            # soup = BeautifulSoup(response.text, 'lxml')
            # data = soup.find_all('table', class_="table_bg001")[1].find('tr').find_all('td')[1].text
            # if ',' in data:
            #     data = str(data).split(',')[0] + str(data).split(',')[1]
            # print('code: %s 总股本: %s, 股价: %s, 总市值:%s' %(i, data, price, float(price) * float(data)))
            # RRXInnerMobileDBMgr.save_push_result(tablename='financial_report',
            #                                      condition={'code': i},
            #                                      result_type='price_list',
            #                                      result={'update_time': update_time, 'price': price}
            #                                      )
            # RRXInnerMobileDBMgr.save_set_result(tablename='financial_report',
            #                                     condition={'code': i},
            #                                     result_type='type',
            #                                     result=type
            #                                     )
            # except KeyError:
            #     print('已经停盘，code为%s' % code)


if __name__ == '__main__':
    code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600100",
                 "600104", "600111", "600340", "600485", "600518", "600519", "600547", "600606", "600837",
                 "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
                 "601198", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
                 "601601", "601628", "601668", "601688", "601766", "601788", "601800", "601818", "601857",
                 "601881", "601901", "601985", "601988", "601989",'600019', '600309', '601669', '601878', '603993']
    for code in code_list:
        install_daily_sharepirce(code)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/22 下午5:18
    Author  : Richard Chen
    File    : PE_jisuan.py
    Software: IntelliJ IDEA
'''

from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr

def PE_Calculation():
    pass


if __name__ == '__main__':
    new_code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600019",
                     "600104", "600111", "600340", "600309", "600518", "600519", "600547", "600606", "600837",
                     "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
                     "601669", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
                     "601601", "601628", "601668", "601688", "601766", "601878", "601800", "601818", "601857",
                     "601881", "603993", "601985", "601988", "601989"]
    report_list = []
    market_list = []
    for code in new_code_list:
        code_data = LmInnerReportDBMgr.get_code_data('lm_stock_data', code)
        if not code_data['isHalt']:
            market_list.append(float(code_data['history_price_stock'][-1]['total_market']))
        else:
            market_list.append(float(code_data['history_price_stock'][-1]['total_market']))
            # for i in code_data['history_price_stock']:
            #     if i['date'] == '2017-12-27':
            #         market_list.append(float(i['total_market']))

        for i in range(4):
            report_list.append(float(code_data['report']['lrb'][i]['SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN']))
    print(sum(market_list))
    print(sum(report_list))
    print(sum(market_list) / sum(report_list))


        #
        # market_data.append(float(code_data['history_price_stock'][-1]['total_market']))
        # print(code,float(code_data['history_price_stock'][-1]['total_market']))
        # o = code_data['report']['lrb'][0]['SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN']
        # t = code_data['report']['lrb'][1]['SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN']
        # th = code_data['report']['lrb'][2]['SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN']
        # f = code_data['report']['lrb'][3]['SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN']
    #     one += o
    #     two += t
    #     three += th
    #     four += f
    # print('2017第三季度', one)
    # print('2017第二季度', two)
    # print('2017第一季度', three)
    # # print('2016第四季度', four)
    # print('和:', one + two + three)



        # if code in ['600309','601989']:
        #     market_data.append(float(code_data['history_price_stock'][-1]['total_market']))
        # for i in code_data['history_price_stock']:
        #     if i['date'] == '2017-12-22':
        #         market_data.append(float(i['total_market']))

    #
    # print(len(market_list))
    # print(market_list)
    # print(report_list)
    # market = 0
    # report = 0
    # for i in report_list:
    #     report += float(i)
    # for n in market_list:
    #     market += n
    # print(market)
    # print(report)
    # print(market / report)

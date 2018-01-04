#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午5:44
    Author  : Richard Chen
    File    : stock_crawler_inner_db.py
    Software: IntelliJ IDEA
'''

from common.db_utils.base_data_crawler_db import BaseCrawlerDB, RichardDBConn


class LmInnerReportDBMgr(BaseCrawlerDB):
    def __init__(self):
        BaseCrawlerDB.__init__(self)

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_code_data(tablename, code):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        find_part = {'code': code}
        ret = mg_conn[tablename].find_one(find_part)
        return ret

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_code(tablename, code, result_type):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        find_part = {'code': code}
        ret = mg_conn[tablename].find_one(find_part)
        if ret:
            try:
                return ret[result_type]
            except KeyError:
                return None

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_all_code(tablename):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        data = mg_conn[tablename].find()
        data_list = []
        for i in data:
            data_list.append(i['code'])
        return data_list

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def del_code_list_data(tablename, condition, del_data):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        data = mg_conn[tablename].find_one(condition)
        data['code_list'].remove(del_data)
        update_part = {"$set": {'code_list': data['code_list']}}
        mg_conn[tablename].update(condition, update_part, upsert=True)

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_financial_report_teble(tablename, condition, tables):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        data = mg_conn[tablename].find_one(condition)
        table_list = data['report'][tables]
        return table_list

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_index_comstock_teble(tablename, condition, tables):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        data = mg_conn[tablename].find_one(condition)
        table_list = data['component_stock_dict'][tables]
        return table_list

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_index_comstock_data(tablename, condition,):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        data = mg_conn[tablename].find_one(condition)
        table_list = data['component_stock_dict']
        return table_list

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_data_list(tablename, condition,result_type):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        data = mg_conn[tablename].find_one(condition)
        table_list = data[result_type]
        return table_list

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def cc(tablename):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        # data = mg_conn[tablename].find({'code': '600000'},
        #                                {"data": {"$elemMatch": {"date": "2017-12-01"}}})

        data = mg_conn[tablename].install({'code': '600000'},{'$push':{'data.1':{'dd':123}}})
        for i in data:
            print(i)




if __name__ == '__main__':
    # data = LmInnerReportDBMgr.get_financial_report_teble('lm_stock_data', {'code': '600000'},'lrb')
    # print(data)
    d = LmInnerReportDBMgr.get_index_comstock_teble('lm_index_data',{'code':'000016'},'2017-12-11')
    print(d)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午5:22
    Author  : Richard Chen
    File    : base_data_crawler_db.py
    Software: IntelliJ IDEA
'''

from datetime import datetime
from common.utils import time_utils
from common.db_utils.db_conn_annotation import RichardDBConn




class BaseCrawlerDB(object):
    def __init__(self):
        pass

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_data(tablename, condition):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        data = mg_conn[tablename].find_one(condition)
        return data

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_table_all(tablename):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        return mg_conn[tablename].find()

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def save_push_result(tablename, condition, result_type, result):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        update_part = {"$push": {result_type: result}}
        mg_conn[tablename].update(condition, update_part, upsert=True)

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def save_set_result(tablename, condition, result_type, result):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        update_part = {"$set": {result_type: result}}
        mg_conn[tablename].update(condition, update_part, upsert=True)

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def save_insert_result(tablename, result):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        mg_conn[tablename].insert_one(result)

    @staticmethod
    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
    def get_table_count(tablename):
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        return mg_conn[tablename].count()
if __name__ == '__main__':
    pass
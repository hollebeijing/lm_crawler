#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午5:04
    Author  : Richard Chen
    File    : db_conn_annotation.py
    Software: IntelliJ IDEA
'''
from contextlib import contextmanager
from common.db_utils.connection import BaseConn, MongoConn, RedisConn, SQLAlchemyConn
from common.thread_utils.thread_local import ThreadLocal


class RichardDBConn:
    sqlalchemy = 'sqlalchemy'
    redis = 'redis'
    mongo = 'mongo'

    def __init__(self):
        pass

    @staticmethod
    def auto_connection(connection=None, **user_params):
        def decorating_func(func):
            def wrapper(*args, **kwargs):
                db_conn = None
                if connection is None:
                    db_conn = None
                elif RichardDBConn.redis == connection.lower():
                    db_conn = RedisConn.get_connection(**user_params)
                elif RichardDBConn.sqlalchemy == connection.lower():
                    db_conn = SQLAlchemyConn.get_connection(**user_params)
                elif RichardDBConn.mongo == connection.lower():
                    db_conn = MongoConn.get_connection(**user_params)

                if connection is not None:
                    ThreadLocal.set_val(connection, db_conn)

                if connection is None or db_conn is None:
                    pass
                    # print ({'desc': '请求连接名称: ' + str(connection) + ', 取得连接为空(None)'})

                try:
                    return func(*args, **kwargs)
                finally:
                    if db_conn is not None:
                        BaseConn.close(db_conn)
                        # logging.debug({'desc': '释放' + str(connection) + '数据库连接资源完毕'})

            wrapper.__name__ = func.__name__
            return wrapper

        return decorating_func

    @staticmethod
    def get_connection(connection=None):
        # print {'descs': '取得' + str(connection) + '数据库连接'}
        return ThreadLocal.exists(connection) and ThreadLocal.get_val(connection) or None

    @staticmethod
    @contextmanager
    def open(connection=None):
        conn = RichardDBConn.get_connection(connection)
        yield conn
        BaseConn.close(conn)


'''

以下是使用示例:
connection: 指定连接类型
添加注解后, 可以使用RrxDBConn.get_connection(connection)方法取得一个数据库连接, 方法执行完毕后会自动释放连接(如果手动close也无影响)

'''



'''
使用多重注解一次获取多种连接
'''


@RichardDBConn.auto_connection(connection=RichardDBConn.redis, host='10.10.159.12', port=6379, db=3)
@RichardDBConn.auto_connection(connection=RichardDBConn.mongo)
def get_multi_conn():
    r_conn = RichardDBConn.get_connection(RichardDBConn.redis)
    mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)

    print(r_conn.keys('common*'))
    print(mg_conn['anti_fraud_cache_data'].find_one({"cache_token": "geo_mobile_three_items_match"}))


'''
在嵌套方法体内获取连接
'''


@RichardDBConn.auto_connection(connection=RichardDBConn.redis, host='10.10.159.12', port=6379, db=3)
def get_inner_conn():
    r_conn = RichardDBConn.get_connection(RichardDBConn.redis)
    print(r_conn.keys('common*'))

    @RichardDBConn.auto_connection(connection=RichardDBConn.mongo, host='10.10.159.12', port=27017, db='rrx_anti_fraud_deploy',
                               user='test_user', passwd='test_user_pass')
    def my_test():
        mg_conn = RichardDBConn.get_connection(RichardDBConn.mongo)
        print(mg_conn['anti_fraud_cache_data'].find_one({"cache_token": "geo_mobile_three_items_match"}))

    return my_test()


'''
使用with ... open语法获取连接
'''



if __name__ == "__main__":
    # get_data()

    # for i in range(0, 200):
    #     threading.Thread(target=get_data).start()

    # get_multi_conn()

    # get_inner_conn()

    import time

    while True:
        time.sleep(10)

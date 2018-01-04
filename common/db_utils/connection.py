#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午5:07
    Author  : Richard Chen
    File    : connection.py
    Software: IntelliJ IDEA
'''

import logging
import json
import traceback
import threading
import redis


from pymongo import MongoClient
from pymongo.database import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from conf.db_settings import *

class BaseConn(object):
    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        pass

    @staticmethod
    def close(connection):
        if hasattr(connection, 'close') and not isinstance(connection, Database):
            try:
                connection.close()
            except Exception as e:
                logging.exception(
                    json.dumps({
                        'desc': '连接资源关闭异常',
                        'exception': traceback.format_exc(e)}, ensure_ascii=False, indent=0))


# # redis连接管理对象
class RedisConn(BaseConn):
    """
        Redis连接管理类，负责建立Redis连接
        获取连接对象：conn = RedisConn.get_connection()
        获取连接对象的方法已进行多线程同步, 为线程安全方法

        查看redis当前连接数 info clients
        查看redis支持最大连接数 config get maxclients
    """

    __established_pool = {}
    __lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    @contextmanager
    def open(host=redis_host, port=redis_port, db=redis_db,
             socket_keepalive=True, retry_on_timeout=True):
        redis_conn = RedisConn.get_connection(host, port, db, socket_keepalive, retry_on_timeout)
        yield redis_conn

    # 取得连接, 相同的ip和port会共用一个连接池
    @staticmethod
    def get_connection(host=redis_host, port=redis_port, db=redis_db,
                       socket_keepalive=True, retry_on_timeout=True):
        key = str(host) + ':' + str(port)
        if key in RedisConn.__established_pool:
            return redis.Redis(connection_pool=RedisConn.__established_pool[key])
        else:
            RedisConn.__lock.acquire()
            if key not in RedisConn.__established_pool:
                RedisConn.__established_pool[key] = redis.ConnectionPool(host=host, port=port, db=db,
                                                                         socket_keepalive=socket_keepalive,
                                                                         retry_on_timeout=retry_on_timeout)
            RedisConn.__lock.release()
            return redis.Redis(connection_pool=RedisConn.__established_pool[key])

#
# # SQL ORM连接管理对象
class SQLAlchemyConn(BaseConn):
    # 连接池管理(key值为host:port)
    __established_pool = {}
    __lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    @contextmanager
    def open(host=sqlalchemy_host, port=sqlalchemy_port, db=sqlalchemy_db,
             user=sqlalchemy_user, passwd=sqlalchemy_passwd,
             pool_size=sqlalchemy_pool_size, max_overflow=sqlalchemy_max_overflow,
             pool_recycle=sqlalchemy_pool_recycle,
             autocommit=False, autoflush=False, convert_unicode=True, use_pool=True):
        sqlalchemy_conn = SQLAlchemyConn.get_connection(host, port, db, user, passwd,
                                                        pool_size, max_overflow, pool_recycle,
                                                        autocommit, autoflush, convert_unicode, use_pool)

        yield sqlalchemy_conn

        if sqlalchemy_conn is not None:
            sqlalchemy_conn.close()
            # logging.info('释放SQLAlchemy数据库连接资源完毕')

    @staticmethod
    def get_connection(host=sqlalchemy_host, port=sqlalchemy_port, db=sqlalchemy_db,
                       user=sqlalchemy_user, passwd=sqlalchemy_passwd,
                       pool_size=sqlalchemy_pool_size, max_overflow=sqlalchemy_max_overflow,
                       pool_recycle=sqlalchemy_pool_recycle,
                       autocommit=False, autoflush=False, convert_unicode=True, use_pool=True):

        if use_pool:
            """
                从用户自定义连接池取得连接, 相同的ip和port会共用一个连接池(连接使用完毕, 需要显式调用close方法将连接放回连接池)
            """
            key = str(host) + ':' + str(port)
            if key in SQLAlchemyConn.__established_pool:
                return sessionmaker(autocommit=autocommit, autoflush=autoflush, bind=SQLAlchemyConn.__established_pool[key])()

            # 进行多线程同步, 保证一个程序实例只有一个连接池对象
            SQLAlchemyConn.__lock.acquire()
            if key not in SQLAlchemyConn.__established_pool:
                mysql_alchemy_uri = "mysql://%s:%s@%s:%d/%s?charset=utf8&use_unicode=0" % (user, passwd, host, port, db)
                SQLAlchemyConn.__established_pool[key] = create_engine(mysql_alchemy_uri,
                                                                       convert_unicode=True,
                                                                       pool_size=pool_size,
                                                                       max_overflow=max_overflow,
                                                                       pool_recycle=pool_recycle)
            SQLAlchemyConn.__lock.release()
            return sessionmaker(autocommit=autocommit, autoflush=autoflush, bind=SQLAlchemyConn.__established_pool[key])()
        else:
            """
                取出自定义连接(连接使用完毕, 需要显式调用close方法将释放连接)
            """
            mysql_alchemy_uri = "mysql://%s:%s@%s:%d/%s?charset=utf8&use_unicode=0" % (user, passwd, host, port, db)
            eg = create_engine(mysql_alchemy_uri, poolclass=NullPool)
            return sessionmaker(autocommit=autocommit, autoflush=autoflush, bind=eg)()

# mongo连接管理对象
class MongoConn(BaseConn):
    __established_pool = {}
    __lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    @contextmanager
    def open(host=mongo_host, port=mongo_port, db=mongo_db,
             user=mongo_user, passwd=mongo_passwd,
             is_auth=mongo_is_auth):
        mongo_conn = MongoConn.get_connection(host, port, user, passwd, db, is_auth)
        yield mongo_conn

    @staticmethod
    def get_connection(host=mongo_host, port=mongo_port, db=mongo_db,
                       user=mongo_user, passwd=mongo_passwd,
                       is_auth=mongo_is_auth):
        key = str(host) + ':' + str(port)

        if key in MongoConn.__established_pool:
            # 提升MongoClient对象获取速度
            mg_client = MongoConn.__established_pool[key]
        else:
            MongoConn.__lock.acquire()
            if key not in MongoConn.__established_pool:
                try:
                    mg_client = MongoClient(host, port, connect=True)
                    MongoConn.__established_pool[key] = mg_client
                except Exception as e:
                    logging.error('爬虫系统建立数据库连接异常', msg_type='rrx_crawler')
                    raise e
                finally:
                    MongoConn.__lock.release()
            else:
                mg_client = MongoConn.__established_pool[key]

        connection = mg_client[db]
        if is_auth:
            try:
                # 进行连接授权
                # 弊端是每次执行数据库操作相同会话请求都多一次身份认证请求，性能有要求时，可以进行调整
                # 好处是在该处设置监控点可以监控到数据库操作过程中的网络异常问题，而不需要在分散的各个数据库操作点添加监控
                connection.authenticate(user, passwd)
            except Exception as e:
                logging.error('爬虫系统认证数据库[%s]异常' % db)
                raise e
        return connection


if __name__ == '__main__':
    pass
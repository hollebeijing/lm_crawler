#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午5:16
    Author  : Richard Chen
    File    : thread_local.py
    Software: IntelliJ IDEA
'''

from __future__ import absolute_import

import threading

_local_map = threading.local()
_common_key = 'common_thread_data'
setattr(_local_map, _common_key, {})


class ThreadLocal:
    def __init__(self):
        pass

    @staticmethod
    # 获取线程变量map对象
    def get_local_map():
        return _local_map

    @staticmethod
    # 设置线程变量属性值
    def set_val(key, val):
        setattr(_local_map, key, val)

    @staticmethod
    # 获取线程变量属性值
    def get_val(key):
        return getattr(_local_map, key)

    @staticmethod
    # 设置公共线程变量属性值
    def hset_common_val(key, val):
        getattr(_local_map, _common_key)[key] = val

    @staticmethod
    # 获取公共变量属性值
    def hget_common_val(key):
        return getattr(_local_map, _common_key)[key]

    @staticmethod
    # key值是否存在
    def exists(key):
        return hasattr(_local_map, key)

    @staticmethod
    # 删除属性值
    def remove(key):
        if hasattr(_local_map, key):
            delattr(_local_map, key)

    @staticmethod
    # 删除公共属性值
    def hmove(key):
        c_map = getattr(_local_map, _common_key)
        if c_map.has_key(key):
            c_map.pop(key)


'''
以下是测试示例:
'''
if __name__ == '__main__':
    # 设置公共属性值
    ThreadLocal.hset_common_val('token_1', 'local_val_1')
    # 获取公共属性值
    print(ThreadLocal.hget_common_val('token_1'))
    print(getattr(_local_map, _common_key).keys())
    print('\r\n')


    # 设置公共属性值
    ThreadLocal.hset_common_val('token_2', 'local_val_2')
    # 获取公共属性值
    print(ThreadLocal.hget_common_val('token_2'))
    print(getattr(_local_map, _common_key).keys())
    print('\r\n')

    # 设置用户自定义值
    ThreadLocal.set_val('my_dict_1', {'a': 'b'})
    # 获取用户自定义值
    print(ThreadLocal.get_val('my_dict_1'))
    print('\r\n')

    # 删除公共属性值
    ThreadLocal.hset_common_val('token_3', 'local_val_3')
    print(ThreadLocal.hget_common_val('token_3'))
    ThreadLocal.hmove('token_3')
    print(ThreadLocal.hget_common_val('token_3'))


    # 删除用户自定义值
    ThreadLocal.set_val('my_dict_2', {'a': 'b'})
    print(ThreadLocal.exists('my_dict_2'))
    ThreadLocal.remove('my_dict_2')
    print(ThreadLocal.exists('my_dict_2'))
    print('\r\n')

    # 打印当前线程变量中的所有元素
    print(_local_map.__dict__)


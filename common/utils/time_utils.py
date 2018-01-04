#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午5:23
    Author  : Richard Chen
    File    : time_utils.py
    Software: IntelliJ IDEA
'''
import time, datetime
from datetime import timedelta


def get_current_time(format=None):
    if format is not None:
        return time.strftime(format)
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S')


def get_current_date(format=None):
    if format is not None:
        return time.strftime(format)
    else:
        return time.strftime('%Y-%m-%d')


def tranfer_any_time(some_date):
    if "年" in some_date:
        return time.strptime(str(some_date), '%Y年%m月%d日')
    else:
        return time.strptime(str(some_date), '%Y.%m.%d')


def tranfer_time_to_localtime(some_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(some_time))


def get_between_date_arr(start_date, end_date):
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    oneday = datetime.timedelta(days=1)
    res_arr = []
    while start_date_obj <= end_date_obj:
        res_arr.append(datetime.datetime.strftime(start_date_obj, "%Y-%m-%d"))
        start_date_obj = start_date_obj + oneday
    return res_arr


def get_date_scope(end_date_diff_day, pre_num):
    today = datetime.datetime.today()
    end_day = today - datetime.timedelta(days=end_date_diff_day)
    start_day = end_day - datetime.timedelta(days=pre_num)
    return (datetime.datetime.strftime(start_day, "%Y-%m-%d"), datetime.datetime.strftime(end_day, "%Y-%m-%d"))


def cal_pre_date(today, pre_days):
    start_date_obj = datetime.datetime.strptime(today, '%Y-%m-%d')
    diff_days = datetime.timedelta(days=pre_days)
    return datetime.datetime.strftime(start_date_obj - diff_days, "%Y-%m-%d")


def get_delta_date(days=0, minutes=0, seconds=0):
    query_time = datetime.datetime.now() - timedelta(days=days, minutes=minutes, seconds=seconds)
    query_time = query_time.strftime("%Y-%m-%d %H:%M:%S")
    return query_time


def get_microsecond_timestamp():
    """
    :return: current timestamp with microsecond as int, like 1489485552246
    """
    cur_time = datetime.datetime.now()
    timestamp = int(time.mktime(cur_time.timetuple()) * 1000.0 + cur_time.microsecond / 1000.0)
    return timestamp


def date_turn_timestamp(date1, date2):
    date1 = time.mktime(time.strptime(date1, "%Y-%m-%d"))
    date2 = time.mktime(time.strptime(date2, "%Y-%m-%d"))
    if date1 >= date2:
        return True
    return False


def date_timestamp(date, format_str='%Y-%m-%d'):
    return time.mktime(time.strptime(date, format_str))


def timestamp_date(date, format_str='%Y-%m-%d'):
    time_local = time.localtime(date)
    return time.strftime(format_str, time_local)


def get_date_object(date, format_str='%Y-%m-%d'):
    return datetime.datetime.strptime(date, format_str)


def get_today_date(format_str='%Y-%m-%d'):
    now = datetime.datetime.now()
    return now.strftime(format_str)


def getEveryDay(begin_date, end_date, type):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    if type:
        return date_list
    else:
        return date_list[1:]


if __name__ == "__main__":
    # print(getEveryDay('2004-01-02', '2005-12-31', 1))  #第一次获取
    # print(getEveryDay('2006-01-01', '2007-12-31', 1))  #第二次获取
    # print(getEveryDay('2008-01-01', '2009-12-31', 1))  #第二次获取
    # print(getEveryDay('2010-01-01', '2011-12-31', 1))  #第二次获取
    # print(getEveryDay('2012-01-01', '2013-12-31', 1))  #第二次获取
    print(getEveryDay('2014-01-01', '2015-12-31', 1))  #第二次获取

    # print(getEveryDay('2017-03-20','2017-05-25',  0))
    # 2014616 ，20141215，201371
    # cmd = 7
    # if cmd == 1:
    #     print(get_current_time())
    # elif cmd == 2:
    #     print(tranfer_any_time("2015年09月12日"))
    #     print(tranfer_any_time("2015.09.12"))
    #     print(get_current_date())
    #     start_date = "2016-05-29"
    #     end_date = "2016-06-04"
    #     print(get_between_date_arr(start_date, end_date))
    # elif cmd == 3:
    #     print(get_date_scope(1, 6))
    # elif cmd == 4:
    #     print(cal_pre_date("2016-07-01", 1 - 1))
    #     print(cal_pre_date("2016-07-01", 7 - 1))
    #     print(cal_pre_date("2016-07-01", 30 - 1))
    # elif cmd == 5:
    #     # print get_delta_date(minutes=-12*60)
    #     print(get_delta_date(days=-1))
    # elif cmd == 6:
    #     print(get_microsecond_timestamp())
    # elif cmd == 7:
    #     print(get_date_object('2017-09-30').day)

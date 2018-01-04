#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/2 下午2:55
    Author  : Richard Chen
    File    : d.py
    Software: IntelliJ IDEA
'''

# d = ['600000.XSHG',
#      '600004.XSHG',
#      '600006.XSHG',
#      '600008.XSHG',
#      '600009.XSHG',
#      '600011.XSHG',
#      '600015.XSHG',
#      '600016.XSHG',
#      '600019.XSHG',
#      '600026.XSHG',
#      '600028.XSHG',
#      '600029.XSHG',
#      '600030.XSHG',
#      '600033.XSHG',
#      '600036.XSHG',
#      '600038.XSHG',
#      '600050.XSHG',
#      '600098.XSHG',
#      '600100.XSHG',
#      '600104.XSHG',
#      '600171.XSHG',
#      '600221.XSHG',
#      '600350.XSHG',
#      '600569.XSHG',
#      '600591.XSHG',
#      '600597.XSHG',
#      '600601.XSHG',
#      '600602.XSHG',
#      '600609.XSHG',
#      '600637.XSHG',
#      '600642.XSHG',
#      '600643.XSHG',
#      '600649.XSHG',
#      '600652.XSHG',
#      '600664.XSHG',
#      '600688.XSHG',
#      '600705.XSHG',
#      '600717.XSHG',
#      '600795.XSHG',
#      '600805.XSHG',
#      '600808.XSHG',
#      '600811.XSHG',
#      '600812.XSHG',
#      '600832.XSHG',
#      '600839.XSHG',
#      '600863.XSHG',
#      '600887.XSHG',
#      '600895.XSHG',
#      '600900.XSHG']
# import hashlib
# import json
#
# data = hashlib.md5()

#新浪财报
import requests
from conf.requests_useragent import get_user_agent
#
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': get_user_agent(),
}
# res = requests.get(
#     url='http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/600002/ctrl/all.phtml',
#     headers=headers,
# )
#
# print(res.text)
import json

url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600591,day,2002-01-01,2010-01-31,320,qfq'
res = requests.get(
    url=url,
    headers=headers,
)
print(json.loads(res.text)['data']['sh600591']['qt']['sh600591'][1])
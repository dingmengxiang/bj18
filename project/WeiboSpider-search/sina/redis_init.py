#!/usr/bin/env python
# encoding: utf-8
import redis
import sys
import os
import datetime
import pymysql
import re
sys.path.append(os.getcwd())


r = redis.Redis(host='10.1.195.143', port=6379, db=0, password='samVW!$#jh')

conn=pymysql.connect(host = 'rm-bp1163rl4802767s8.mysql.rds.aliyuncs.com',db='market_spider',user='sam',passwd='samVW!$#jh')
cursor = conn.cursor()
cursor.execute("select movie_name from movie_info where show_time like '2017%中国大陆%'")
names = str(cursor.fetchall())
name = re.findall("\('(.*?)',\)",names)
url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=time&page=1"
# 搜索的关键词，可以修改

for key in name:
    keyword = "《{}》+电影".format(key)
    # 搜索的起始日期，可修改
    date_start = datetime.datetime.strptime("2017-01-01", '%Y-%m-%d')
    # 搜索的结束日期，可修改
    date_end = datetime.datetime.strptime("2018-11-19", '%Y-%m-%d')
    time_spread = datetime.timedelta(days=1)
    while date_start < date_end:
        next_time = date_start + time_spread
        url = url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"))
        print(url)
        r.lpush('weibo_spider:start_urls', url)
        date_start = next_time
        print('添加{}成功'.format(url))

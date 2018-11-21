# -*- coding: utf-8 -*-
import time
LOG_FILE = time.strftime('%Y%m%d',time.localtime(time.time()))+'.log'

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False
# DEFAULT_REQUEST_HEADERS = {
# 'Cookie': '_T_WM=414d2aac6c20dbbe3b8d1a0df2462c7c; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHg_LLU7QqKYOxNeflnxqGUcJi4HQN8AHdnJnh92oEjBY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGwFKTw7cNWVmgbZEEX_0s5JpX5K-hUgL.FoqNeKn7eoeEe0q2dJLoIE5LxK.L1KnLB.qLxKqL1KqLB-qLxK.LBK2LB.9.Mcx0qBtt; MLOGIN=1; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; SUB=_2A252zfoIDeRhGeBP6lcX9CzLwzuIHXVSMYZArDV6PUJbkdAKLVjXkW1NRZQT4z4oyeZUojhlxUbB_XTu6SjsIFNu; SUHB=0gHizexxnXOuK9; SSOLoginState=1539934808; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076032062377061',
# 'Host': 'weibo.cn'
#  }


# CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 根据账号池大小调整 目前的参数是账号池大小为200

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0.1

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'sina.middlewares.CookieMiddleware': 500,
   'sina.middlewares.RedirectMiddleware': 200,
}


ITEM_PIPELINES = {
     'sina.pipelines.MysqlPipeline':300,
}
#
#MYSQL配置
MYSQL_HOST = 'gz-cdb-l4r5h3m3.sql.tencentcdb.com'
MYSQL_PORT = 61928
MYSQL_DBNAME = 'market_spider'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'samVW!$#jh'

# Redis 配置
# LOCAL_REDIS_HOST = '10.1.195.143'
# LOCAL_REDIS_PORT = 6379
# REDIS_PARAMS =  {
#             'password': 'samVW!$#jh'
#         }

# Ensure use this Scheduler
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"

# Redis URL
#REDIS_URL = 'redis://{}:{}'.format(LOCAL_REDIS_HOST, LOCAL_REDIS_PORT)

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 31

# Persist
SCHEDULER_PERSIST = True
REDIRECT_ENABLED = True

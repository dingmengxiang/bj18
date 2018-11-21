# -*- coding: utf-8 -*-

# Scrapy settings for WeiBo project
import random
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WeiBo'

SPIDER_MODULES = ['WeiBo.spiders']
NEWSPIDER_MODULE = 'WeiBo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'WeiBo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 10
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = True

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
# 'Cookie': '_T_WM=414d2aac6c20dbbe3b8d1a0df2462c7c; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHg_LLU7QqKYOxNeflnxqGUcJi4HQN8AHdnJnh92oEjBY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGwFKTw7cNWVmgbZEEX_0s5JpX5K-hUgL.FoqNeKn7eoeEe0q2dJLoIE5LxK.L1KnLB.qLxKqL1KqLB-qLxK.LBK2LB.9.Mcx0qBtt; MLOGIN=1; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; SUB=_2A252zfoIDeRhGeBP6lcX9CzLwzuIHXVSMYZArDV6PUJbkdAKLVjXkW1NRZQT4z4oyeZUojhlxUbB_XTu6SjsIFNu; SUHB=0gHizexxnXOuK9; SSOLoginState=1539934808; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076032062377061',
# 'Host': 'weibo.cn'
#  }
# # #
# cookie_list=[ '_T_WM=414d2aac6c20dbbe3b8d1a0df2462c7c; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHg_LLU7QqKYOxNeflnxqGUcJi4HQN8AHdnJnh92oEjBY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGwFKTw7cNWVmgbZEEX_0s5JpX5K-hUgL.FoqNeKn7eoeEe0q2dJLoIE5LxK.L1KnLB.qLxKqL1KqLB-qLxK.LBK2LB.9.Mcx0qBtt; MLOGIN=1; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; SUB=_2A252zfoIDeRhGeBP6lcX9CzLwzuIHXVSMYZArDV6PUJbkdAKLVjXkW1NRZQT4z4oyeZUojhlxUbB_XTu6SjsIFNu; SUHB=0gHizexxnXOuK9; SSOLoginState=1539934808; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076032062377061']
#
#
# headers = {
#             'Cookie':random.choice(cookie_list),
#
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'WeiBo.middlewares.WeiboSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
   #'WeiBo.middlewares.WeiboSpiderMiddleware': 543,
  # 'WeiBo.middlewares.UserAgentMiddleware': 43,
#}
DOWNLOADER_MIDDLEWARES = {
    'WeiBo.middlewares.UserAgentMiddleware': None,
#    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'WeiBo.middlewares.CookieMiddleware':501,
   'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
'WeiBo.middlewares.WeiboSpiderMiddleware':500
}
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'WeiBo.pipelines.WeiboPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPERROR_ALLOWED_CODES = [301,302]
REDIRECT_ENABLED = False


DOWNLOAD_TIMEOUT = 1
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 3
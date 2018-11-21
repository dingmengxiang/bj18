# -*- coding: utf-8 -*-

# Scrapy settings for TianYanCha project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

BOT_NAME = 'TianYanCha'

SPIDER_MODULES = ['TianYanCha.spiders']
NEWSPIDER_MODULE = 'TianYanCha.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TianYanCha (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'TianYanCha.middlewares.MyproxiesSpiderMiddleware': 200,
#    'TianYanCha.middlewares.UserAgentMiddleware': 300
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'TianYanCha.middlewares.MyproxiesSpiderMiddleware': 200,
   # 'TianYanCha.middlewares.RedirectMiddleware': 100,
   'TianYanCha.middlewares.UserAgentMiddleware': 300
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'TianYanCha.pipelines.TianyanchaPipeline': 300,
}

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

# 连接本地MySQL
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'market_spider'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'

DOWNLOAD_TIMEOUT = 7
# 重新请求
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 10

# 添加重定向状态码
RETRY_HTTP_CODES = [302]

# 添加HTTP码
HTTPERROR_ALLOWED_CODES = [302, 403]

# 关掉重定向, 不会重定向到新的地址
REDIRECT_ENABLED = False

# 启用日志
# LOG_ENABLED = True
LOG_FILE = time.strftime('%Y%m%d', time.localtime(time.time())) + '.log'
# LOG_LEVEL = 'DEBUG'

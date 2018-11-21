# -*- coding: utf-8 -*-

# Scrapy settings for YiChe project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
LOG_FILE = time.strftime('%Y%m%d',time.localtime(time.time()))+'.log'

BOT_NAME = 'YiChe'

SPIDER_MODULES = ['YiChe.spiders']
NEWSPIDER_MODULE = 'YiChe.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'YiChe (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
DOWNLOADER_MIDDLEWARES = {
   'YiChe.middlewares.YicheSpiderMiddleware': 543,
    'YiChe.middlewares.UserAgentMiddleware':443,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'YiChe.middlewares.TooManyRequestsRetryMiddleware': 900,
}
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'YiChe.middlewares.YicheSpiderMiddleware': 543,
#}
ITEM_PIPELINES = {
   'YiChe.pipelines.YichePipeline': 300,
}
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'YiChe.middlewares.YicheDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'YiChe.pipelines.YichePipeline': 300,
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
MYSQL_HOST = 'tidb.maizuo.com'
MYSQL_PORT = 4000
MYSQL_DBNAME = 'market_spider'
MYSQL_USER = 'marketing'
MYSQL_PASSWD = 'c131dVQYFqNI2rum'




DOWNLOAD_TIMEOUT =70
# 重新请求
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES=3
COMPANY_FROM = '易车网'
HTTPERROR_ALLOWED_CODES = [301,302]
DOWNLOAD_DELAY = 1
RETRY_HTTP_CODES = [429,427,407,502]
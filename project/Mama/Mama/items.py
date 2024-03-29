# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MamaItem(scrapy.Item):
    url = scrapy.Field()  # 文章网址
    title = scrapy.Field()  # 文章标题
    # author=scrapy.Field()           #文章作者
    content = scrapy.Field()  # 文章内容
    create_time = scrapy.Field()  # 文章发表时间
    has_img = scrapy.Field()  # 是否有图

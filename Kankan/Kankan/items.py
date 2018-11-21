# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KankanItem(scrapy.Item):
    # define the fields for your item here like:
      title = scrapy.Field()
      create_time = scrapy.Field()
      url = scrapy.Field()
     # name = scrapy.Field()
      content = scrapy.Field()
      has_img = scrapy.Field()  # 是否有图
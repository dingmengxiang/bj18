# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanchaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    industry = scrapy.Field()
    url = scrapy.Field()
    excel_id = scrapy.Field()
    mobile = scrapy.Field()

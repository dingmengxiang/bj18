# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AstrosinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    constellation = scrapy.Field()
    #date = scrapy.Field()
    health_num = scrapy.Field()
    luck_crystal = scrapy.Field()
    luck_color = scrapy.Field()    #幸运颜色
    luck_num = scrapy.Field()    #幸运指数
    noble_con = scrapy.Field()  #贵人星座
    today_remind = scrapy.Field()
    is_do = scrapy.Field()
    not_do = scrapy.Field()


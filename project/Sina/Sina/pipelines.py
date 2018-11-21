# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import time
class SinaPipeline(object):
    def process_item(self, item, spider):
        wb = Workbook()
        ws = wb.active
        ws.append(
            ['代码', '名称', '最新价', '今日涨跌幅', '净额(主力)', '净占比(主力)', '净额(超大单)', '净占比(超大单)', '净额(大单)', '净占比(大单)', '净额(中单)',
             '净占比(中单)', '净额(小单)', '净占比(小单)', '时间'])
        line = item['data']
        ws.append(line)  # 将数据以行的形式添加到xlsx中
        try:
            wb.save('f:\\20181013.xlsx')
        except Exception as result:
            print("捕获到异常:%s" % result)
            time.sleep(3)



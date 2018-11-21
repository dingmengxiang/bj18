# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

class EastmoneyPipeline(object):
    def __init__(self):
        self.get_item = 0
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append([ '代码','名称','最新价','今日涨跌幅','净额(主力)','净占比(主力)','净额(超大单)','净占比(超大单)','净额(大单)','净占比(大单)','净额(中单)','净占比(中单)','净额(小单)','净占比(小单)','时间'])  # 设置表头
    def process_item(self, item, spider):
        line = item["data"]
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.get_item =self.get_item + 1
        print('数据插入成功第%d'%self.get_item)
        self.wb.save('e:\\20181011.xlsx')  # 保存xlsx文件
        return item

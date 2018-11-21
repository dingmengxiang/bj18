# -*- coding: utf-8 -*-
import scrapy
import re
from EastMoney.items import EastmoneyItem

class EastmoneySpider(scrapy.Spider):
    name = 'eastmoney'
    allowed_domains = ['eastmoney.com']

    def start_requests(self):
        for i in range(1,75):
            start_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p= %d &ps=50&data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA'%i
            print('***************************')
            print("开始抓取第%d页"%i)
            print('***************************')
            yield scrapy.Request(start_url,
                                 callback=self.parse)
    def parse(self, response):
        text=response.text
        data_list = re.findall('"(.*?)"',text)
        print(data_list)
        for data in data_list:
            item = EastmoneyItem()
            list = data.split(",")[1:-1]
            item["data"] = list
            yield item


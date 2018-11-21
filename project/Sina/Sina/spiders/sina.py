# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
from Sina.items import SinaItem
import time

class SinaSpider(scrapy.Spider):
    name = 'sina'
   # allowed_domains = ['sina.com']
    def start_requests(self):
        for i in range(1,2):
            start_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={}&num=40&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=init'.format(i)
            yield scrapy.Request(
                start_url,
                callback=self.parse
            )

    def parse(self, response):
        text = response.text
        symbol_list = re.findall('symbol:"(.*?)"',text)
        print(symbol_list)
        for symbol in symbol_list:
            url = 'http://finance.sina.com.cn/realstock/company/%s/nc.shtml'%symbol
            yield scrapy.Request(
                url,
                callback=self.page
            )
   # def page(self,response):
        #print(response.url)
        # driver = webdriver.Chrome()
        # item = SinaItem()
        # driver.get(response.url)
        # a = driver.find_elements_by_xpath('//div[@id="MRFlow"]//tbody/tr[2]/td')
        # b = driver.find_elements_by_xpath('//div[@id="MRFlow"]//tbody/tr[3]/td')
        # c = driver.find_elements_by_xpath('//div[@id="FLFlow"]//tbody/tr[2]/td')
        # d = driver.find_elements_by_xpath('//div[@id="FLFlow"]//tbody/tr[3]/td')
        # e = driver.find_elements_by_xpath('//div[@id="FLFlow"]//tbody/tr[4]/td')
        # f = a + b + c + d + e
        # data = []
        # for i in f:
        #     data.append(i.text)
        # item['data'] = data
        # yield item
        #
        # wb = Workbook()
        # ws = wb.active
        # ws.append(
        #     ['代码', '名称', '最新价', '今日涨跌幅', '净额(主力)', '净占比(主力)', '净额(超大单)', '净占比(超大单)', '净额(大单)', '净占比(大单)', '净额(中单)',
        #      '净占比(中单)', '净额(小单)', '净占比(小单)', '时间'])
        # line = data
        # ws.append(line)  # 将数据以行的形式添加到xlsx中
        # try:
        #     wb.save('f:\\20181011.xlsx')
        # except Exception as result:
        #     print("捕获到异常:%s" % result)
        #     time.sleep(3)
        #     driver.quit()

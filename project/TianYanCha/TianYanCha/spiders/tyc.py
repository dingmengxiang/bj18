# -*- coding: utf-8 -*-

import scrapy
from TianYanCha.items import TianyanchaItem
from TianYanCha.get_com_name import ComInfo
from urllib.parse import quote


class TycSpider(scrapy.Spider):
    name = 'tyc'
    com = ComInfo()
    com.put_info()
    que_com = com.que_com

    def start_requests(self):
        while not self.que_com.empty():
            info = dict(self.com.get_com_info())
            key, = info
            com_name = str(key)
            url_name = quote(com_name, 'utf-8')
            search_url = 'https://m.tianyancha.com/search?key=%s' % url_name
            print("当前搜索的是：{} 链接为：".format(com_name))
            print(search_url)
            detail_list = info[com_name]
            id = detail_list[0]
            mobile = detail_list[1]
            yield scrapy.Request(url=search_url, callback=self.parse, dont_filter=True, meta={'id': id, 'mobile': mobile})

    def parse(self, response):
        id = response.meta['id']
        mobile = response.meta['mobile']
        url_info = response.xpath('//div[@class="search_result_container"]/div[1]//div[@class="col-xs-10 search_name pl0 pr0"]/a/@href').extract()

        if url_info:
            print("当前获得的链接为： {}".format(url_info[0]))
            yield scrapy.Request(url=url_info[0], callback=self.parse_item, dont_filter=True, meta={'id': id, 'mobile': mobile})
        else:
            print("获取详情页出错，链接为 {}".format(response.url))

    def parse_item(self, response):
        item = TianyanchaItem()
        name = response.xpath('//div[@class="f18 new-c3 float-left"]/text()').extract()
        industry = response.xpath('//div[@class="content-container pb10"]/div[5]/span[2]/text()').extract()
        if industry:
            print("当前解析的的是：{} 链接为：".format(name[0]))
            print(response.url)
            item['url'] = str(response.url)
            item['name'] = str(name[0])
            item['industry'] = str(industry[0])
            item['excel_id'] = response.meta['id']
            item['mobile'] = response.meta['mobile']
            yield item
        else:
            print("获取页面错误")

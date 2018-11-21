# -*- coding: utf-8 -*-
import scrapy
from AstroSina.items import AstrosinaItem
import re
import datetime
class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com']
    start_urls = ['http://sina.com/']
    def start_requests(self):
        list = ['Aries','Taurus','Gemini','Cancer','leo','Virgo',
                'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
        for i in list:
            start_url = 'http://astro.sina.com.cn/fate_day_%s/'%i

            yield scrapy.Request(start_url,
                                 callback=self.parse)
    def parse(self, response):
        item = AstrosinaItem()
        i = datetime.datetime.now()
        item['constellation'] =  response.xpath('//div[@class="tit_n"]/text()').extract_first()
        date = response.xpath('//div[@class="time"]/text()').extract_first()
        #item["date"] = i.year
        #item['date'] = ''.join(re.findall('有效日期：(\d+)-(\d+)-(\d+)',date)[0])
        item['health_num'] = response.xpath('//table[@class="tb"]//tr[3]/td[2]/text()').extract_first()
        item['luck_crystal'] = response.xpath('//table[@class="tb"]//tr[3]/td[4]/text()').extract_first()
        item['luck_color'] = response.xpath('//table[@class="tb"]//tr[4]/td[2]/text()').extract_first()
        item['luck_num'] = response.xpath('//table[@class="tb"]//tr[4]/td[4]/text()').extract_first()
        item['noble_con'] = response.xpath('//table[@class="tb"]//tr[5]/td[2]/text()').extract_first()
        today_remind = response.xpath('//div[@class="words"]/p[1]/text()').extract_first()
        item['today_remind'] = re.findall('今日提醒：(.*)',today_remind)[0]
        is_do = response.xpath('//div[@class="words"]/p[2]/text()').extract_first()
        item['is_do'] = re.findall('去做：(.*)',is_do)[0]
        not_do = response.xpath('//div[@class="words"]/p[3]/text()').extract_first()
        item['not_do'] = re.findall('别做：(.*)',not_do)[0]

        yield item

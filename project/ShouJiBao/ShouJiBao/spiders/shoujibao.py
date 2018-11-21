# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ShouJiBao.items import ShoujibaoItem
import re
import redis
import json
from ShouJiBao import settings
class ShoujibaoSpider(CrawlSpider):
    name = 'shoujibao'
    allowed_domains = ['shoujibao.cn']
    start_urls = ['http://www.shoujibao.cn/news/']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.shoujibao.cn/news/show-htm-itemid-\d+\.html'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/news/index-htm-page-\d+\.html'), follow=True),

    )

    def parse_item(self, response):
        item = ShoujibaoItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item['title'] = response.xpath('//h1[@id="n_title"]/text()').extract_first()
        item['url'] = response.url
        time= response.xpath('//span[@class="time"]/text()').extract_first()
        item['create_time'] =''.join( re.findall('(\d+)-(\d+)-(\d+)',time)[0])
        is_img = response.xpath('//div[@id="content"]//img/@src').extract()[:-1]
        content = response.xpath('//div[@class="content"]').extract_first()
        item['content'] = self.clean(content)

        if len(is_img) > 0:
            item['has_img'] = 1
            for img in is_img:
                newUrl = self.redis_push(img)
                a = re.findall('(.*)' + str(img) + '(.*)', item['content'], re.S)
                try:
                    item['content'] = a[0][0] + str(newUrl) + a[0][1]
                except:
                    continue

        else:
            item['has_img'] = 0
        yield item
        print(item)
    def redis_push(self, url):
        r = redis.Redis(host='10.1.195.143', port=6379, db=0, password='samVW!$#jh')
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=123456)
        if url.startswith('http'):
            oldUrl = url
        else:
            oldUrl = "http://" + url
        key = hash(url)
        fileName = str(key) + '.jpg'
        newUrl = "http://img.market.maizuo.com/" + str(key) + '.jpg'
        source = settings.COMPANY_FROM
        data = {
            'fileName': fileName,
            'oldUrl': oldUrl,
            'newUrl': "http://img.market.maizuo.com/" + fileName,
            'sourceName': source,
        }
        json_data = json.dumps(data)
        r.lpush('IMG_ALI_OSSs', json_data)
        return newUrl

    def clean(self, s):

        s = re.sub('<div style=".*?"', '', s)
        s = re.sub('<img src="http://www.shoujibao.cn/images/sjb_wx.jpg".*?>', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)
        s = re.sub('style=".*?"','',s)
        s = re.sub('（.*?）', '', s)
        delete = ['据外媒报道，','本报.*?报道','【编者按】','年','月','日','记者','手机报.*?，','北京时间.*?，','报道.*?，']
        for key in delete:
            s = re.sub(key,'',s)
        return s

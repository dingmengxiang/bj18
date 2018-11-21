# -*- coding: utf-8 -*-
import scrapy
from ItHome.items import IthomeItem
import re
import redis
import json
from ItHome import settings

class IthomeSpider(scrapy.Spider):
    name = 'ithome'
    allowed_domains = ['ithome.com']
    start_urls = ['https://www.ithome.com/ithome/getajaxdata.aspx?page=1&type=indexpage']

    def parse(self, response):
        # item = IthomeItem()
        # item['url'] = response.url
        # print(item)
        #分组
         url_list = response.xpath('//ul[@class="ulcl"]/li/a/@href').extract()

         for url in url_list:
             yield scrapy.Request(
                 url,
                 callback=self.parse_detail,
             )
         for i in range(500,1500):
             next_url = 'https://www.ithome.com/ithome/getajaxdata.aspx?page={0}&type=indexpage'.format(i)
             yield scrapy.Request(next_url,callback=self.parse)
    def parse_detail(self,response):
        item=IthomeItem()
        item['url'] = response.url
        item['title']  = response.xpath('//div[@class="post_title"]/h1/text()').extract_first()
        time = response.xpath('//div[@class="post_title"]/span/span[1]/text()').extract_first()
        item['create_time']= ''.join(re.findall('(\d+)-(\d+)-(\d+)',time)[0])
        content=''.join(response.xpath('//div[@class="post_content"]/p').extract())
        item['content'] = self.clean(content)
        
        is_img = response.xpath('//div[@class="post_content"]//img/@src').extract()
        print(is_img)
        # if len(is_img) > 0:
        #     item['has_img'] = 1
        #     for img in is_img:
        #         newUrl = self.redis_push(img)
        #         a = re.findall('(.*)' + str(img) + '(.*)', item['content'], re.S)
        #         try:
        #             item['content'] = a[0][0] + str(newUrl) + a[0][1]
        #         except:
        #             continue
        #
        # else:
        #     item['has_img'] = 0
        # yield item


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
#        s = re.sub('<img src="http://www.shoujibao.cn/images/sjb_wx.jpg".*?>', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)
        s = re.sub('style=".*?"', '', s)
        s = re.sub('（.*?）', '', s)
        delete = ['搜索', '关注', '官方微博', '微信公众号', '年','月', '日' , '北京时间.*?，', '报道.*?，','IT之家.*?，']
        for key in delete:
            s = re.sub(key, '', s)
        return s

        #item['create_time']=time


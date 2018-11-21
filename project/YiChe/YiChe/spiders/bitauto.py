# -*- coding: utf-8 -*-
import scrapy
import re
import json
from YiChe.items import YicheItem
import redis
from YiChe import settings

class BitautoSpider(scrapy.Spider):
    name = 'bitauto'
    allowed_domains = ['bitauto.com']
    start_urls = ['http://news.bitauto.com/views3/news/tagnewsjsonlist?cid=1088&pageIndex=1']

    def parse(self, response):

        text  =  response.text
        text = json.loads(text)
        for i in range(20):
           item = YicheItem()
           item['url'] = text[i]['url']
           item['title'] = text[i]['title']
           create_time= text[i]['publishTimeFormat']
           item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',create_time)[0])
           #print(item)
           yield scrapy.Request(item['url'],
                                callback=self.detail,
                                meta={"item":item}
                              )

        for p in range(2,501):
            next_url = 'http://news.bitauto.com/views3/news/tagnewsjsonlist?cid=1088&pageIndex={0}'.format(p)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def detail(self,response):
        item = response.meta["item"]
        # item['url'] = response.url
        # item['title'] = response.xpath('//article/h1/text()').extract_first()
        content =''.join( response.xpath('//div[@class="article-content motu_cont"]/p').extract())
        is_img = response.xpath('//div[@class="article-content motu_cont"]//img/@src').extract()
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
        s = re.sub('<span .*?></span>', '', s)
        s = re.sub('<div style=".*?"', '', s)
        s = re.sub('<b>.*?</b>', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)
        s = re.sub('<strong>.*?</strong>', '', s)
        s = re.sub('style=".*?"', '', s)
        s = re.sub('<script .*?>', '', s)
        delete = ['易车网.*?，', '(.*?)', '【编者按】', '年', '月', '日', '记者', '北京时间.*?，', '报道.*?，']
        for key in delete:
            s = re.sub(key, '', s)
        return s





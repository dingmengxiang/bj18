# -*- coding: utf-8 -*-
import scrapy
from YuLe.items import YuleItem
import re
import redis
from YuLe import settings
import json


class YuleSpider(scrapy.Spider):
    name = 'yule'
    allowed_domains = ['yule.com']

    def start_requests(self):
        for i in range(300000, 330000):
            next_url = 'http://yule.360.cn/content/{0}?from=infoflow'.format(i)
            yield scrapy.Request(next_url,
                                 callback=self.parse,
                                 )

    def parse(self, response):

            item = YuleItem()
            item['title'] = response.xpath('//h1[@id="content-title"]/text()').extract_first()
            create_time = response.xpath('//p[@class="source-time"]/text()').extract_first()
            try:
              item['create_time'] = ''.join(re.findall('\n.*?(\d+)-(\d+)-(\d+)',str(create_time))[0])
            except:
                pass
            item['url'] = response.url
            is_img = response.xpath('//div[@class="content"]//img/@src').extract()
            content = ''.join(response.xpath('//div[@class="content"]/p').extract())
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
        git = []
        s = re.sub('style=".*?"', '', s)
        s = re.sub('<strong>.*?</strong>', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)
        s = re.sub('（.*?）', '', s)
        s = re.sub('\(.*?\)', '', s)
        delete = [ '年', '月', '日', '时', '分', '责任编辑.*']
        for w in delete:
            s = re.sub(w, '', s)
        return s
#item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)', create_time)[0])


# -*- coding: utf-8 -*-
import scrapy
import re
import json
from She.items import SheItem
import redis
from She import settings
from She.langconv import *
class SheSpider(scrapy.Spider):
    name = 'she'
    allowed_domains = ['she.com']
    def start_requests(self):
        url = 'https://www.she.com/wp-json/she-rest-api/getLatestArticles/'
        for i in range(10):
            yield scrapy.FormRequest(
                url=url,
                formdata={'category':'241988','page':str(i)},
                callback=self.parse
            )

    def parse(self, response):
        text= response.text
        text = json.loads(text)
        list = text.get('items')
        for item_one in list:
            item = SheItem()
            item['create_time'] = item_one['post_date_gmt']
            item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',item['create_time'])[0])
            item['title'] = item_one['post_title']
            item['title'] = self.Traditional2Simplified(item['title'])
            item['url'] = item_one['url']
            # print(time)
            # print(title)
            # print(url)
        # time = re.findall('"post_date_gmt\":(.*?) ',text)
        # print(time)
            yield scrapy.Request(
                item['url'],
                callback=self.detail,
                meta={"item":item}
            )
    def detail(self,response):
        item = response.meta["item"]

        item['content'] = response.xpath('//div[@id="segment-area"]/segment').extract_first()
        item['content'] = self.clean(item['content'])
        item['content'] = self.Traditional2Simplified(item['content'])
        is_img = response.xpath('//div[@id="segment-area"]/segment/p/img/@src').extract()

        if len(is_img) >0:
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
        s = re.sub('style=".*?"', '', s)
        s = re.sub('<strong>.*?</strong>', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)

        delete = ['年','月','日','时','分']
        for w in delete:
            s = re.sub(w, '', s)
        return s
    def Traditional2Simplified(self, sentence):
        sentence = Converter('zh-hans').convert(sentence)
        return sentence
# -*- coding: utf-8 -*-
import scrapy
from MovieYam.items import MovieyamItem
import re
import redis
import json
from MovieYam import settings
from MovieYam.langconv import *
class YamSpider(scrapy.Spider):
    name = 'yam'
    allowed_domains = ['yam.com']
    def start_requests(self):
        for i in range(50,100):
            start_url = 'https://movie.yam.com/Ent/News?page={}'.format(i)
            yield scrapy.Request(
                start_url,
                callback=self.parse
            )

    def parse(self, response):
        li_list = response.xpath('//div[@id="News"]/ul/li')
        for li in li_list:
            href = li.xpath('./div[@class="Content right"]/a/@href').extract_first()
            url = 'https://movie.yam.com' +  href
            yield scrapy.Request(
                url,
                callback=self.detail
            )
    def detail(self,response):
        item = MovieyamItem()
        item['url'] = response.url
        a = response.xpath('//div[@class="data"]/div[@class="date"]/text()').extract_first()
        b = re.findall('(.*?\.)', a)

        duiying = {'Dec.': '12', 'Nov.': '11', 'Oct.': '10', 'Sep.': '09', 'Aug.': '08', 'Jul.': '07', 'Jun.': '06',
                   'May.': '05', 'Apr.': '04', 'Mar.': '03', 'Fab.': '02', 'Jan.': '01'}
        keys = list(duiying.keys())
        for key in keys:

            if key == b[0]:
                mouth = duiying[key]
                new = re.sub('.*?\.', str(mouth), a)

                time = re.findall('(\d+) (\d+)', new)
                time = time[0][1] + time[0][0]
                item['create_time'] = time

        item['title'] = response.xpath('//div[@class="data"]/h1/text()').extract_first()
        item['title'] = self.Traditional2Simplified(item['title'])
        item['content'] = response.xpath('//div[@class="articleCon"]').extract_first()
        item['content']=self.clean(item['content'])
        item['content'] = self.Traditional2Simplified(item['content'])
        is_img = response.xpath('//div[@class="articleCon"]/div//img/@src').extract()
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

    def clean(self, content):
        content = re.sub('<span.*?>', '', content)
        content = re.sub('style=".*?"', '', content)
        content = re.sub(r"style=\\'.*?'", '', content)
        content = re.sub('</span>', '', content)
        content = re.sub('<a .*?>', '', content)
        content = re.sub('<iframe.*?>', '', content)
        content = re.sub('class=".*?"', '', content)

        delete = ['年', '月', '日']
        for w in delete:
            content = re.sub(w, '', content)

        return content
    def Traditional2Simplified(self, sentence):
        sentence = Converter('zh-hans').convert(sentence)
        return sentence
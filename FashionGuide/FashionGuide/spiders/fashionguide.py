# -*- coding: utf-8 -*-
import scrapy
import  re
from FashionGuide.items import FashionguideItem
import json
import redis
from FashionGuide import settings
from FashionGuide.langconv import *
from urllib.parse import quote

class FashionguideSpider(scrapy.Spider):
    name = 'fashionguide'
    #allowed_domains = ['fashionguide.com']
    def start_requests(self):
        for i in range(1,100):
            start_url = 'https://fgblog.fashionguide.com.tw/content/news/page/{}'.format(i)
            yield scrapy.Request(
                start_url,
                callback=self.parse
            )

    def parse(self, response):
        div_list = response.xpath('//div[@class="row no-margin"]/div[@class="col-12 col-lg-6 no-padding"]')
        for div in div_list:
            item = FashionguideItem()
            item['url'] = div.xpath('./div[@class="post-item"]//a/@href').extract_first()
            title= div.xpath('./div[@class="post-item"]//a/h5/text()').extract_first()
            item['title'] = self.Traditional2Simplified(title)
            yield scrapy.Request(
                item['url'],
                callback=self.detail,
                meta={'item': item}
            )
    def detail(self,response):
        item = response.meta['item']
        a=response.xpath('//div[@class="author-name"]/span[2]/text()').extract_first()

        b = re.findall('(.{1,2})月', a)

        duiying = {'十二': '12', '十一': '11', '十': '10', '九': '09', '八': '08', '七': '07', '六': '06', '五': '05', '四': '04',
                   '三': '03', '二': '02', '一': '01'}
        keys = list(duiying.keys())
        for key in keys:

            if key == b[0]:
                mouth = duiying[key]

                new = re.sub('.{1,2}月', str(mouth), a)
                time = ''.join(re.findall('(\d+) (\d+), (\d+)', new)[0])
                time = time[4:8] + time[0:4]
                item['create_time'] = time

        content = str(response.xpath('//div[@class="article-content"]/p').extract())

        if content=='[]':
            content = str(response.xpath('//div[@class="article-content"]//div[@class="column"]/p').extract())
            #print(content)
            item['content'] = content
            is_img = response.xpath('//div[@class="article-content"]/p//img/@src').extract()

            if is_img == []:
                is_img = response.xpath('//div[@class="article-content"]//div[@class="column"]/p//img/@src').extract()
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
            else:

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
            item['content'] = self.Traditional2Simplified(item['content'])
            item['content'] = self.clean(item['content'])
            yield item
        else:
            #print(content)
            item['content'] = content
            is_img = response.xpath('//div[@class="article-content"]/p//img/@src').extract()

            if is_img == []:
                is_img = response.xpath('//div[@class="article-content"]//div[@class="column"]/p//img/@src').extract()
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
            else:


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
            item['content'] = self.Traditional2Simplified(item['content'])
            item['content'] = self.clean(item['content'])
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

        delete = ['年', '月', '日','图片来源.*','图片、资料来源.*']
        for w in delete:
            content = re.sub(w, '', content)

        return content

    def Traditional2Simplified(self, sentence):
        sentence = Converter('zh-hans').convert(sentence)
        return sentence

    '''def start_requests(self):
        for i in range(100,151):
            start_url = 'https://fgblog.fashionguide.com.tw/category/0/today_hot_posts/?page={}'.format(i)
            yield scrapy.Request(
                start_url,
                callback=self.parse
            )
    def parse(self, response):
        # href_list = response.xpath('//div[@class="fg-card-list"]/div[@class="fg-card"]/a/@href').extract()
        # title = response.xpath('//div[@class="fg-card-list"]/div[@class="fg-card"]/a/@href').extract()
        # for href in href_list:
        div_list = response.xpath('//div[@class="fg-card-list"]/div[@class="fg-card"]')
        for div in div_list:
            item = FashionguideItem()
            item['url'] = div.xpath('./a/@href').extract_first()

            title = div.xpath('./div/ul/li[@class="fg-card-middle"]/a/text()').extract_first()
            item['title'] = self.Traditional2Simplified(title)

            yield  scrapy.Request(
                item['url'],
                callback=self.detail,
                meta = {'item':item}
            )
    def detail(self,response):
        item = response.meta['item']
        time = response.xpath('//div[@class="post-date"]/text()').extract_first()
        item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',time)[0])
        content = str(response.xpath('//div[@class="article-content"]/p').extract())
        item['content'] = self.clean(content)
        is_img = response.xpath('//div[@class="article-content"]/p//img/@src').extract()
        if len(is_img)>0:
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
        item['content'] = self.Traditional2Simplified(item['content'])
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
    def clean(self,content):
        content = re.sub('<span.*?>','',content)
        content = re.sub('style=".*?"','',content)
        content = re.sub(r"style=\\'.*?'", '', content)
        content = re.sub('</span>','',content)
        content = re.sub('<a .*?>','',content)
        content = re.sub('<iframe.*?>', '', content)

        delete = ['年','月','日']
        for w in delete:
            s = re.sub(w, '', content)

        return content
    def Traditional2Simplified(self,sentence):
        sentence = Converter('zh-hans').convert(sentence)
        return sentence'''




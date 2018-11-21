# -*- coding: utf-8 -*-
import scrapy
import re
from Cosmopolitan.items import CosmopolitanItem
import json
import redis
from Cosmopolitan import settings
from Cosmopolitan.langconv import *
class CosmopolitanSpider(scrapy.Spider):
    name = 'cosmopolitan'
    #allowed_domains = ['cosmopolitan.com']
    def start_requests(self):
        for i in range(1,200,10):
            start_url = 'https://www.cosmopolitan.com.hk/action/page/3399/{}/10'.format(i)
            yield scrapy.Request(
                start_url,
                callback=self.parse
            )

    def parse(self, response):
        href_list = response.xpath('//div[@class="TwoCol"]/div/figure/a/@href').extract()
        for href in href_list:
            url = 'https://www.cosmopolitan.com.hk'+href
            yield scrapy.Request(
                url,
                callback=self.detail
            )
    def detail(self,response):
        item = CosmopolitanItem()
        text = response.text
        item['url'] = response.url
        time = response.xpath('//time/@datetime').extract_first()
        duiying = {'Dec': '12', 'Nov': '11', 'Oct': '10', 'Sep': '09', 'Aug': '08', 'Jul': '07', 'Jun': '06',
                   'May': '05', 'Apr': '04', 'Mar': '03', 'Fab': '02', 'Jan': '01'}
        a= str(re.findall('\d+-(.*?)-\d+',time)[0])

        b=re.sub(a,duiying[a],time)
        item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',b)[0])

        item['title'] = response.xpath('//article[@data-first-read="true"]/div[2]/div[@class="StickyArticle"]/div[1]/h1/text()').extract_first()
        item['title'] = self.Traditional2Simplified(item['title'])
        content = ''.join(response.xpath('//div[@class="StickyArticle"]').extract())
        item['content'] = content
        is_img = response.xpath('//div[@class="StickyArticle"]//img/@data-src').extract()
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
        item['content'] = self.Traditional2Simplified(item['content'])
        item['content'] = self.clean(item['content'])
        yield item
    def redis_push(self, url):
        r = redis.Redis(host='10.1.195.143', port=6379, db=0, password='samVW!$#jh')
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=123456)
        if url.startswith('http'):
            oldUrl = url
        else:
            oldUrl = "https://www.cosmopolitan.com.hk" + url
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

        s = re.sub('class=".*?"', '', s)
        #        s = re.sub('<img src="http://www.shoujibao.cn/images/sjb_wx.jpg".*?>', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('href=\'.*?\'', '', s)
        s = re.sub('</a>', '', s)
        s = re.sub('<iframe.*?>', '', s)
        s = re.sub('style=".*?"', '', s)
        s = re.sub('style=\'.*?\'', '', s)
        s = re.sub('（.*?）', '', s)
        delete = ['年', '月', '日','\*完整内容.*','编辑部','【.*?】']
        for key in delete:
            s = re.sub(key, '', s)
        return s
    def Traditional2Simplified(self,sentence):
        sentence = Converter('zh-hans').convert(sentence)
        return sentence

# -*- coding: utf-8 -*-
import scrapy
import re
import json
from Btime.items import BtimeItem
import redis
from Btime import settings
class BtimeSpider(scrapy.Spider):
    name = 'btime'

    def start_requests(self):
        i = 76403
        for m in range(0,1000):
            i = i + 2
            start_url= 'https://pc.api.btime.com/btimeweb/getInfoFlow?&channel=news&request_pos=channel&citycode=local_440300_440000&refresh=2&req_count=2&refresh_type=2&pid=3&from=haojrrd&page_refresh_id=86f8b918-bc94-11e8-b633-0cc47a56f672&_=15374206{0}'.format( i)
            yield scrapy.Request(start_url,callback=self.parse)





    def parse(self, response):

        text = response.text.replace('\\', '')
        url_list=re.findall('"open_url":"(https:.*?)"',text)
        for url in url_list:
            yield scrapy.Request(url,callback=self.page)
    def page(self,response):
        item = BtimeItem()
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@id="title"]/text()').extract_first()
        time = response.xpath('//span[@class="col time"]/text()')
        if time is not None:
             time = response.xpath('//span[@class="col time"]/text()').extract_first()
             item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',str(time))[0])

        else:

             time = response.xpath('//span[@class="time"]/text()').extract_first()
             item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)', str(time))[0])
        content=''.join(response.xpath('//div[@class="content-text"]//p').extract())
        item['content'] = self.clean(content)
        is_img =response.xpath('//div[@class="content-text"]//p/img/@src').extract()

        if len(is_img) >0:
            item['has_img'] = 1
            for img in is_img:
                print(img)
                newUrl = self.redis_push(img)
                a = re.findall('(.*)' + str(img) + '(.*)', item['content'], re.S)
                try:
                    item['content'] = a[0][0] + str(newUrl) + a[0][1]
                except:
                    continue
        else:
            item['has_img'] = 0

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
        git = []
        s = re.sub('style=".*?"', '', s)
        s = re.sub('<strong>.*?</strong>', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)
        s = re.sub('（.*?）', '', s)
        s = re.sub('\(.*?\)', '', s)
        delete =['中新网.*?，','据.*?报道','新华社.*?电','年','月','日','时','分','责任编辑.*',]
        for w in delete:
            s = re.sub(w, '', s)
        return s


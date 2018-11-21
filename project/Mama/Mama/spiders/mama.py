# -*- coding: utf-8 -*-
import scrapy
from Mama.items import MamaItem
from Mama import settings
import json
import redis
import re
class MamaSpider(scrapy.Spider):
    name = 'mama'
    allowed_domains = ['mama.cn']
    start_urls = ['http://www.mama.cn/z/wiki/life/?n=1']

    def parse(self, response):
        #分组
        li_list=response.xpath("//ul[@class='wiki-article-list']/li")
        for li in li_list:
            item = MamaItem()
            item['url']=li.xpath("./h3/a[@target='_blank']/@href").extract_first()
            item['title']=li.xpath("./h3/a[@target='_blank']/text()").extract_first()

            yield scrapy.Request(
                item['url'],
                callback=self.parse_detail,
                meta={"item":item}
            )
        for i in range(0,1745):
            next_url = "http://www.mama.cn/z/wiki/life/?n={}".format(i)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
    def parse_detail(self,response):
        item = response.meta["item"]
        content=''.join(response.xpath("//div[@class='mod-ctn']/p").extract())
        item['create_time'] = 0
        is_img=response.xpath("//div[@class='mod-ctn']//img/@src").extract()
        # delete = ['style=".*?"', '<strong>.*?</strong>', '<a.*?>', '</a>']
        # for key in delete:
        #     content = re.sub(key, '', content, re.S)
        #     item['content'] = content
        item['content'] = self.clean(content)

        if len(is_img)>0:
            item['has_img']=1
            for img in is_img:
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
        #r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=123456)
        if url.startswith('http'):
            oldUrl = url
        else:
            oldUrl="http://"+url
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
        return s
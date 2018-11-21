# -*- coding: utf-8 -*-
import scrapy
import re
from Neeu.items import NeeuItem
import json
from Neeu import settings
import redis
class NeeuSpider(scrapy.Spider):
    name = 'neeu'
    allowed_domains = ['neeu.com']

    def start_requests(self):
        for i in range(1,100):
            start_url = 'https://www.neeu.com/articles/page/{}'.format(i)
            yield scrapy.Request(
            start_url,
            callback=self.parse
        )
    def parse(self, response):
        div_list = response.xpath('//div[@class="grid-item"]')

        for div in div_list:
            item = NeeuItem()
            time = div.xpath('.//span[@class="publish"]/text()').extract_first()
            item['create_time'] = ''.join(re.findall('(\d+)\.(\d+)\.(\d+)',time)[0])
            href = div.xpath('.//div[@class="article-image"]/a/@href').extract_first()
            item['url'] = 'https://www.neeu.com'+href
            item['title']= div.xpath('.//div[@class="article-content"]/h3/a/text()').extract_first()
            yield scrapy.Request(
                item['url'],
                callback=self.detail,
                meta={"item": item}
            )
    def detail(self,response):
        item = response.meta['item']
        content = response.xpath('//div[@class="article-content"]').extract_first()
        item['content'] = self.clean(content)
        is_img = response.xpath('//div[@class="article-content"]//img/@src').extract()

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

        s = re.sub('style=".*?"', '', s)
        s = re.sub('（.*?）', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)

        delete =['年','月','日','详情.*''预定请联络.*?.','更多详情，敬请访问：','访问.*?。','购票方式：.*?。','详情参考请.*']
        for w in delete:
            s = re.sub(w, '', s)
        return s
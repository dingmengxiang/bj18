# -*- coding: utf-8 -*-
import scrapy
import re
from ShSs.items import ShssItem
import json
import redis
from ShSs import settings
class SohuSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    def start_requests(self):
        for i in range(1,51):
            start_url = 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=23&page={}&size=20'.format(i)
            yield scrapy.Request(
            start_url,
            callback=self.parse
        )
    def parse(self, response):
       text = response.text
       id_list = re.findall('"id":(\d+),\s*"authorId":(\d+),',text,re.S)

       for id in id_list:
           url = 'http://www.sohu.com/a/{}_{}'.format(id[0],id[1])
           yield scrapy.Request(
               url,
               callback=self.detail
           )
    def detail(self,response):
        item = ShssItem()
        try:
            item['url'] = response.url
            item['title'] = response.xpath('//div[@class="text-title"]/h1/text()').extract_first()
            time = response.xpath('//span[@id="news-time"]/text()').extract_first()
            item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',time)[0])
            is_img = response.xpath('//article[@id="mp-editor"]//img/@src').extract()
            content = response.xpath('//article[@id="mp-editor"]').extract_first()
            item['content'] = self.clean(content)
            if len(is_img) > 0:
                item['has_img'] =1
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
        except:
            pass


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
       # autoid = re.findall('"autoid":(.*?),',text)
       # for
    def clean(self, s):

        s = re.sub('style=".*?"', '', s)
        s = re.sub('（.*?）', '', s)
        s = re.sub('<a.*?>', '', s)
        s = re.sub('</a>', '', s)

        delete =['原标题：','点击进入搜狐首页','返回搜狐，查看更多','责任编辑：','本文原创于.*?。']
        for w in delete:
            s = re.sub(w, '', s)
        return s
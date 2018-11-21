# -*- coding: utf-8 -*-
import scrapy
import json
from Kankan.items import  KankanItem
import re
import requests
import redis
from Kankan import settings
class KankannewsSpider(scrapy.Spider):
    name = 'kankannews'
    allowed_domains = ['kankanews.com']
    start_urls = ['http://www.kankanews.com/xinwen/']

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.start_parse
        )
    def start_parse(self,response):
        id=response.xpath('//div[@class="left mainBody"]/ul/li/@data-newstime').extract()[-1]


        url = 'http://www.kankanews.com/list/kandian/498?next={}'.format(id)

        yield scrapy.Request(
               url,
            callback=self.parse
        )


    def parse(self, response):


        a=response.text

        b=json.loads(a)
        c=b['list']
        newstime=c[-1]['newstime']
        for list in c:
            item = KankanItem()
            time=list['newsdate']
            time =''.join( re.findall('(\d+)-(\d+)-(\d+)',time)[0])
            item['create_time']=time
            item['title'] = list['title']
            item['url'] = list['titleurl']

            yield scrapy.Request(
                item['url'],
                callback=self.parse_detail,
                meta={"item":item}
            )
        next_url = 'http://www.kankanews.com/list/kandian/498?next={}'.format(newstime)
        if next_url is not None:
             yield scrapy.Request(
                        next_url,
                        callback=self.parse
                 )

    def parse_detail(self,response):
        item =  response.meta["item"]
        content = ''.join(response.xpath("//div[@class='textBody']/p").extract())
        is_img = response.xpath("//div[@class='textBody']//img/@src").extract()
        item['content'] = self.clean(content)
        if len(is_img) >0:
            item["has_img"] =1
            for img in is_img:
                newUrl = self.redis_push(img)
                a = re.findall('(.*)' + str(img) + '(.*)', item['content'], re.S)
                try:
                    item['content'] = a[0][0] + str(newUrl) + a[0][1]
                except:
                    continue

        else:
            item['has_img'] = 0
            # yield item
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
    def clean(self,s):
     s = re.sub('<div style=".*?"', '', s)
     s = re.sub('<a.*?>', '', s)
     s = re.sub('</a>', '', s)
     s = re.sub('class=".*?"', '', s)
     s = re.sub('<param.*?>', '', s)
     s = re.sub('<embed.*?>', '', s)
     s = re.sub('style=".*?"', '', s)
     s = re.sub('<strong>.*?</strong>', '', s)
     delete = [ '看看新闻.{10,100}', '小编第一时间为您划重点，戳图↓',  '实习编辑.*', '截至.*?，', '.{1,2}时', '.{1,2}分', '.{1,2}日', '.{1,2}月','记者.*?，','（.*?）','版权声明.*']
     for key in delete:
         s = re.sub(key, '', s, re.S)
     return s
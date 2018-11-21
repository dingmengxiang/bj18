# -*- coding: utf-8 -*-
import scrapy
from PianDuan.items import PianduanItem
from PianDuan import settings
import re
import redis
from PianDuan.langconv import *
from urllib.parse import quote
import json
class PianduanSpider(scrapy.Spider):
    name = 'pianduan'
    #allowed_domains = ['pianduan.com']

    def start_requests(self):
        for i in range(1,2):
            start_url = 'https://www.pianduan.me/page/{}'.format(i)
            yield scrapy.Request(
                start_url,
                callback=self.parse
            )
    def parse(self, response):
        article_list = response.xpath('//div[@class="row posts-wrapper"]/article')
        for article in article_list:
             href = article.xpath('./div/div[1]/a/@href').extract_first()
             yield scrapy.Request(
                 href,
                 callback=self.detail
             )
    def detail(self,response):
        item = PianduanItem()
        text = response.text

        item['url'] = response.url
        item['title'] = response.xpath('//header[@class="entry-header"]/h1/text()').extract_first()
        time = response.xpath('//div[@class="entry-action"]/div/a/span/text()').extract_first()
        item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',time)[0])
        content = ''.join(re.findall('(<div class="entry-wrapper">.*?)转载请注明',text,re.S)[0])
        #print(content)
        item['content'] = self.clean(content)
        is_img = response.xpath('//div[@class="entry-content u-clearfix"]/p/a/img/@src').extract()

        if len(is_img) > 0:
            item['has_img'] = 1


            for img in is_img:
                newUrl = self.redis_push(img)
                print(newUrl)
                print(img)
                #print(item['content'])
                #item['content']= re.sub(img,'',item['content'],flags=re.S)
                #print(item['content'])
                re.findall(img,item['content'],re.S)
                # try:
                #     item['content'] = a[0][0] + str(newUrl) + a[0][1]
                # except:
                #     continue
        else:
            item['has_img']=0

        # item['content'] = self.Traditional2Simplified(item['content'])
        # item['content'] = self.clean(item['content'])

            # item['content'] = self.Traditional2Simplified(item['content'])
            # item['content'] = self.clean(item['content'])
            # print(item)
            #print(item['content'])
        # else:
        #     is_img = response.xpath('//div[@class="entry-content u-clearfix"]/div/a/img/@src').extract()
        #     if len(is_img) >0 :
        #         for img in is_img:
        #             newUrl = self.redis_push(img)
        #             a = re.findall('(.*)' + str(img) + '(.*)', item['content'], re.S)
        #             try:
        #                 item['content'] = a[0][0] + str(newUrl) + a[0][1]
        #             except:
        #                 continue
        #             print(item['content'])
        #     else:
        #         item['has_img'] = 0
        #     print(item['content'])
        # item['content'] = self.Traditional2Simplified(item['content'])
        # item['content'] = self.clean(item['content'])
        #print(item)

    def clean(self, content):
        content = re.sub('<span.*?>', '', content)
        content = re.sub('style=".*?"', '', content)
        content = re.sub(r"style=\\'.*?'", '', content)
        content = re.sub('</span>', '', content)
        content = re.sub('<a .*?>', '', content)
        content = re.sub('<iframe.*?>', '', content)
        content = re.sub('来源.*', '', content,re.S)
        content = re.sub('年', '', content)
        content = re.sub('月', '', content)
        content = re.sub('日', '', content)



        return content
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
    def Traditional2Simplified(self, sentence):
        sentence = Converter('zh-hans').convert(sentence)
        return sentence

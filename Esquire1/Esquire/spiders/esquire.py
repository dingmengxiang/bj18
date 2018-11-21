# -*- coding: utf-8 -*-
import scrapy
from Esquire.items import EsquireItem
import re
import json
from Esquire import settings
import redis
from Esquire.langconv import *
from urllib.parse import quote


class EsquireSpider(scrapy.Spider):
    name = 'esquire'
    allowed_domains = ['esquire.com']
    def start_requests(self):
        url = 'https://www.esquire.tw/modules/blog/_blog_new_post.php'
        # for n in range(1,7):
        #     for m in range(500,800):
        #         my_formdata = {"pageID":str(m) , "cat":str(n) }
        for i in range(0,100):
            my_formdata  =  {"pageID":str(i)}
            yield scrapy.FormRequest(
                    url,
                    method='POST',
                    formdata = my_formdata,
                    callback=self.parse,
                    dont_filter=True
                )
    def parse(self, response):
        # div_list = response.xpath('//body/div')
        # for div in div_list:
        a_list = response.xpath('//div[@class="head"]/a')

        for  a in a_list:
            item = EsquireItem()
                #time = div.xpath('./div[2]/div[2]/span/text()').extract_first()
                #item['create_time'] = ''.join(re.findall('(\d+)/(\d+)/(\d+)',time)[0])
                #print(item['create_time'])
                # title= div.xpath('./div[2]/div[3]/a/text()').extract_first()
                # item['title'] = self.Traditional2Simplified(title)
            href = a.xpath('./@href').extract_first()

            item['url'] = 'https://www.esquire.tw'+ href



            yield scrapy.Request(
                item['url'],
                callback=self.parse_detail,
                meta={"item":item},
                dont_filter=True
        )
    def parse_detail(self,response):
        item = response.meta["item"]
        title = response.xpath('//h1[@class="head"]/text()').extract_first()
        item['title'] = self.Traditional2Simplified(title)
        time = response.xpath('//span[@class="date"]/text()').extract_first()
        item['create_time'] = ''.join(re.findall('\d+?',time))
        content = ''.join(response.xpath('//div[@class="text"]').extract())
        item['content'] = content
        is_img = response.xpath('//div[@class="text"]//img/@src').extract()
        if len(is_img) > 0:
            item['has_img'] = 1
            for img in is_img:

                img=quote(img,safe='/:?=')

              #  newUrl = self.redis_push(img)
                if len(re.findall('http',img))==1:
                    newUrl = self.redis_push(img)
                else:
                    img1 = 'https://www.esquire.tw' + img
                    newUrl = self.redis_push(img1)
                a = re.findall('(.*)' + str(img) + '(.*)', item['content'], re.S)
                try:
                    item['content'] = a[0][0] + str(newUrl) + a[0][1]
                except:
                    continue

        else:
            item['has_img'] = 0

        item['content'] = self.Traditional2Simplified(item['content'])
        item['content'] = self.clean(item['content'])
        print(item)
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



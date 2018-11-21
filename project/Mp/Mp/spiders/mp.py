# -*- coding: utf-8 -*-
import scrapy
import json
import re
import redis
from Mp import settings
from Mp.items import MpItem
class MpSpider(scrapy.Spider):
    name = 'mp'
    allowed_domains = ['mp.com']
    def start_requests(self):
        for i in range(1,10):
            start_url = 'http://ff.dayu.com/contents/author/08188a5d3a064283ae653ad8cf29a3c4?biz_id=1002&_size=8&_page={}&_order_type=published_at&status=1&_fetch=1&uc_param_str=frdnsnpfvecpntnwprdsssnikt'.format(i)
            yield scrapy.Request(
                start_url,
                callback=self.parse
            )

    def parse(self, response):
        text = response.text
        dict = json.loads(text)
        list = dict['data']
        for div in list:
            item = MpItem()
            try:
               content = div['body']['text']
               #print(content)
               time = div['created_at']
               item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',time)[0])
               item['title'] = div['title']
               item['url'] = 'http://a.mp.uc.cn/article.html?uc_param_str=frdnsnpfvecpntnwprdssskt&from=media#!wm_cid='+ div["content_id"]+'!!wm_aid='+div["origin_id"]+'!!wm_id='+div["author_id"]
               img_list = re.findall('<!--{img:\d+?}-->',content)

               img_url_list = div['body']['inner_imgs']
               item['has_img'] = 1
               for i in range(len(img_list)):
                   newUrl = self.redis_push(img_url_list[i]['url'])
                   content=re.sub(img_list[i],newUrl,content)
               item['content'] = self.clean(content)
               yield item

            except Exception as a:
                pass

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

        # s = re.sub('class=".*?"', '', s)
        # #        s = re.sub('<img src="http://www.shoujibao.cn/images/sjb_wx.jpg".*?>', '', s)
        # s = re.sub('<a.*?>', '', s)
        # s = re.sub('href=\'.*?\'', '', s)
        # s = re.sub('</a>', '', s)
        # s = re.sub('<iframe.*?>', '', s)
        # s = re.sub('style=".*?"', '', s)
        # s = re.sub('style=\'.*?\'', '', s)
        # s = re.sub('（.*?）', '', s)
        delete = ['年', '月', '日']
        for key in delete:
            s = re.sub(key, '', s)
        return s

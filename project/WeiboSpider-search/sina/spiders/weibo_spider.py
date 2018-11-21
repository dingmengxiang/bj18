#!/usr/bin/env python
# encoding: utf-8
import re
from lxml import etree
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider
from sina.items import TweetsItem, InformationItem,CommentItem,Hot_CommentItem
from sina.spiders.utils import time_fix
import time
from urllib.parse import unquote
import redis
import json

class WeiboSpider(RedisSpider):
    name = "weibo_spider"
    base_url = "https://weibo.cn"
    redis_key = "weibo_spider:start_urls"

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        "DOWNLOAD_DELAY": 0.5,
        'REDIS_HOST': '10.1.195.143',
        'REDIS_PORT': 6379,

        # 指定 redis链接密码，和使用哪一个数据库
        'REDIS_PARAMS': {
            'password': 'samVW!$#jh',
        },

    }

    def parse(self, response):

        if response.url.endswith('page=1'):
            # 如果是第1页，一次性获取后面的所有页
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
        """
        解析本页的数据
        """
        tree_node = etree.HTML(response.body)
        # print('***************************')
        # print(response.body)
        # print("***************************")
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            # try:
                tweet_item = TweetsItem()
                url = response.url
                new_url = unquote(url)
                tweet_item['name'] = 'data'
                tweet_item['keyword']=re.findall('keyword=(.*?)&',new_url)[0]
                tweet_item['crawl_time'] = int(time.time())
                tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                tweet_item['weibo_url'] = 'https://weibo.cn/{}/{}'.format(user_tweet_id.group(2),
                                                                           user_tweet_id.group(1))
                tweet_item['_id'] = user_tweet_id.group(2)
                #tweet_item['_id'] = '{}_{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
                create_time_info = tweet_node.xpath('.//span[@class="ct"]/text()')[-1]

                created_at = time_fix(create_time_info.split('来自')[0].strip())

                tweet_item['create_time'] =int(''.join(re.findall('(\d+)-(\d+)-(\d+)',created_at )[0]))
                try:
                    created_from = create_time_info.split('来自')[1].strip()

                    tweet_item['created_from'] = self.ucs(created_from)

                except:
                    tweet_item['created_from'] = ''

                like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[0]
                tweet_item['like_num'] = int(re.search('\d+', like_num).group())

                repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[0]
                tweet_item['repost_num'] = int(re.search('\d+', repost_num).group())
                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[0]
                tweet_item['comment_num'] = int(re.search('\d+', comment_num).group())
                if tweet_item['comment_num'] > 0 :
                    comment = tweet_node.xpath(
                        './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/@href')[0]

                    tweet_item['comment'] = comment

                    yield Request(
                        tweet_item['comment'],
                        callback=self.comment_information
                    )
                  
                else:
                    tweet_item['comment'] = ''

                tweet_content_node = tweet_node.xpath('.//span[@class="ctt"]')[0]
                #检测有没有图片
                img_href = tweet_node.xpath('./div/a[contains(text(),"组图")]/@href')
                if len(img_href) == 1:
                    tweet_item['img_href'] = img_href[0]

                else:
                    tweet_item['img_href'] = ''
                yuantu = tweet_node.xpath('./div[2]/a[2][text()="原图"]/@href')
                if len(yuantu) == 1:
                     url= yuantu[0]
                     img_url = self.redis_push(url)
                     tweet_item['img_url'] = img_url
                else:
                    tweet_item['img_url'] = ''




                # 检测由没有阅读全文:
                all_content_link = tweet_content_node.xpath('.//a[text()="全文"]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield Request(all_content_url, callback=self.parse_all_content, meta={'item': tweet_item},
                                  priority=1)

                else:
                    all_content = tweet_content_node.xpath('string(.)').strip('\u200b')
                    # try:
                    #     # python UCS-4 build的处理方式
                    #     highpoints = re.compile(u'[\U00010000-\U0010ffff]')
                    # except re.error:
                    #     # python UCS-2 build的处理方式
                    #     highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
                    # all_content = highpoints.sub(u'', all_content)
                    tweet_item['content'] = self.ucs(all_content)
                    yield tweet_item
                   # print(tweet_item)


                yield Request(url="https://weibo.cn/{}/info".format(tweet_item['_id']),
                             callback=self.parse_information, priority=2)


            # except Exception as e:
            #     self.logger.error(e)


    def parse_all_content(self, response):
        # 有阅读全文的情况，获取全文
        tree_node = etree.HTML(response.body)
        tweet_item = response.meta['item']
        content_node = tree_node.xpath('//div[@id="M_"]//span[@class="ctt"]')[0]
        all_content = content_node.xpath('string(.)').strip('\u200b')
        # try:
        #     # python UCS-4 build的处理方式
        #     highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        # except re.error:
        #     # python UCS-2 build的处理方式
        #     highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        # all_content = highpoints.sub(u'??', all_content)
        # highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        #all_content = highpoints.sub(u'', all_content)

        tweet_item['content'] = self.ucs(all_content)
        yield tweet_item
       # print(tweet_item)
    def ucs(self,content):
        try:
            # python UCS-4 build的处理方式
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            # python UCS-2 build的处理方式
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        # all_content = highpoints.sub(u'??', all_content)
        # highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        all_content = highpoints.sub(u'', content)
        return all_content

    # def parse_information(self,response):
    #     '''抓取个人信息'''
    #     tweet_item = response.meta["item"]
    #     selector = Selector(response)
    #     text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
    #     nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
    #     gender = re.findall('性别;?[：:]?(.*?);', text1)
    #     place = re.findall('地区;?[：:]?(.*?);', text1)
    #     brief_introduction = re.findall('简介;[：:]?(.*?);', text1)
    #     birthday = re.findall('生日;?[：:]?(.*?);', text1)
    #     sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
    #     sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
    #     vip_level = re.findall('会员等级;?[：:]?(.*?);', text1)
    #     authentication = re.findall('认证;?[：:]?(.*?);', text1)
    #     if nick_name and nick_name[0]:
    #         tweet_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
    #     if gender and gender[0]:
    #         tweet_item["gender"] = gender[0].replace(u"\xa0", "")
    #     if place and place[0]:
    #         place = place[0].replace(u"\xa0", "").split(" ")
    #         tweet_item["province"] = place[0]
    #         if len(place) > 1:
    #             tweet_item["city"] = place[1]
    #     if brief_introduction and brief_introduction[0]:
    #         tweet_item["brief_introduction"] = brief_introduction[0].replace(u"\xa0", "")
    #     if birthday and birthday[0]:
    #         tweet_item['birthday'] = birthday[0]
    #     if sex_orientation and sex_orientation[0]:
    #         if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
    #             tweet_item["sex_orientation"] = "同性恋"
    #         else:
    #             tweet_item["sex_orientation"] = "异性恋"
    #     if sentiment and sentiment[0]:
    #         tweet_item["sentiment"] = sentiment[0].replace(u"\xa0", "")
    #     if vip_level and vip_level[0]:
    #         tweet_item["vip_level"] = vip_level[0].replace(u"\xa0", "")
    #     if authentication and authentication[0]:
    #         tweet_item["authentication"] = authentication[0].replace(u"\xa0", "")
    #     yield Request(url="https://weibo.cn/{}".format(tweet_item['user_id']),
    #                   callback=self.page,
    #                   meta = {'item': tweet_item},
    #                   dont_filter=True, priority=3)
    # def page(self,response):
    #     tweet_item = response.meta["item"]
    #     text = response.text
    #     tweets_num = re.findall('微博\[(\d+)\]', text)
    #     if tweets_num:
    #         tweet_item['tweets_num'] = int(tweets_num[0])
    #     follows_num = re.findall('关注\[(\d+)\]', text)
    #     if follows_num:
    #         tweet_item['follows_num'] = int(follows_num[0])
    #     fans_num = re.findall('粉丝\[(\d+)\]', text)
    #     if fans_num:
    #         tweet_item['fans_num'] = int(fans_num[0])
    #     is_v = response.xpath('//span[@class="ctt"]/img/@alt').extract_first()
    #     if is_v is not None:
    #         tweet_item['is_v'] = 1
    #     else:
    #         tweet_item['is_v'] = 0
    #     print(tweet_item)

        # name = response.xpath('//span[@class="ctt"]/text()').extract_first()
        # fensi = response.xpath('//div[@class="tip2"]/a[2]/text()').extract_first()
        # tweet_item['name'] = name
        # tweet_item['fensi'] = fensi
        # print(tweet_item)
        # tweet_item = response.meta["item"]
        # selector = Selector(response)
        # text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        # nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        # fans_num = re.findall('粉丝\[(\d+)\]', text1)
        # if fans_num:
        #     information_item['fans_num'] = int(fans_num[0])
    # 默认初始解析函数
    def parse_information(self, response):
        """ 抓取个人信息 """
        information_item = InformationItem()

        information_item['name'] = 'information'
        #information_item['crawl_time'] = int(time.time())
        selector = Selector(response)
        information_item['_id'] = re.findall('(\d+)/info', response.url)[0]
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        text2 = selector.xpath('body/div[@class="c"][3]/a//text()').extract()
        if text2:

            b = ','.join(text2[:-1])
            information_item["label"] = b
        else:
            information_item["label"] = ''
        classc = selector.xpath('body/div[@class="c"]').extract()
        if len(classc) == 7:
            school = selector.xpath('body/div[@class="c"][4]/text()').extract()
            school = ','.join(school)
            information_item['school']=school
        else:
            information_item['school']=''

        head_img = selector.xpath('body/div[@class="c"][1]/img/@src').extract_first()
        if head_img:
            information_item["head_img"] = head_img
        else:
            information_item["head_img"] = ''
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        brief_introduction = re.findall('简介;?[：:]?(.*?);', text1)

        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
        vip_level = re.findall('会员等级;?[：:]?(.*?);', text1)
        authentication = re.findall('认证;?[：:]?(.*?);', text1)
        if nick_name and nick_name[0]:
            information_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
        else:
            information_item["nick_name"] = ''
        if gender and gender[0]:
            information_item["gender"] = gender[0].replace(u"\xa0", "")
        else:
            information_item["gender"] = ''
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            information_item["province"] = place[0]
            if len(place) > 1:
                information_item["city"] = place[1]
            else:
                information_item["city"] = ''
        else:
            information_item["province"] = ''
        if brief_introduction and brief_introduction[0]:
            a=self.ucs(brief_introduction[0])
            information_item["brief_introduction"] = a
                #brief_introduction[0].replace(u"\xa0", "")

        else:
            information_item["brief_introduction"] = ''
        if birthday and birthday[0]:
            information_item['birthday'] = birthday[0]
        else:
            information_item['birthday'] = ''
        if sex_orientation and sex_orientation[0]:
            if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
                information_item["sex_orientation"] = "同性恋"
            else:
                information_item["sex_orientation"] = "异性恋"
        else:
            information_item["sex_orientation"] = ''
        if sentiment and sentiment[0]:
            information_item["sentiment"] = sentiment[0].replace(u"\xa0", "")
        else:
            information_item["sentiment"] = ''
        if vip_level and vip_level[0]:
            information_item["vip_level"] = vip_level[0].replace(u"\xa0", "")
        else:
            information_item["vip_level"] = ''
        if authentication and authentication[0]:
            information_item["authentication"] = authentication[0].replace(u"\xa0", "")
        else:
            information_item["authentication"] = ''
        request_meta = response.meta
        request_meta['item'] = information_item
        yield Request(self.base_url + '/u/{}'.format(information_item['_id']),
                      callback=self.parse_further_information,
                      meta=request_meta, dont_filter=True, priority=3)

    def parse_further_information(self, response):

        text = response.text
        information_item = response.meta['item']
        tweets_num = re.findall('微博\[(\d+)\]', text)
        if tweets_num:
            information_item['tweets_num'] = int(tweets_num[0])
        else:
            information_item['tweets_num'] = ''
        follows_num = re.findall('关注\[(\d+)\]', text)
        if follows_num:
            information_item['follows_num'] = int(follows_num[0])
        else:
            information_item['follows_num'] = ''
        fans_num = re.findall('粉丝\[(\d+)\]', text)
        if fans_num:
            information_item['fans_num'] = int(fans_num[0])
        else:
            information_item['fans_num'] = ''
        is_v = response.xpath('//span[@class="ctt"]/img/@alt').extract_first()
        if is_v is not None:
            information_item['is_v'] = 1
        else:
            information_item['is_v'] = 0
        yield information_item
        #print(information_item)


    def comment_information(self,response):
        a = response.url

        uid = re.findall('uid=(.*?)&', a)[0]

        string = re.findall('comment/(.*?)\?', a)[0]
        weibo_url = 'https://weibo.cn/' + uid + '/' + string
        div_list = response.xpath('//body/div[@class="c"][contains(@id,"C_")]')


        for div in div_list:
            comment_item = CommentItem()
            comment_item['_id'] = uid

            comment_item['weibo_url'] = weibo_url

            commenter_url = div.xpath('./a/@href').extract_first()
            comment_item['commenter_url'] = 'https://weibo.cn'+commenter_url
            comment_item['name'] = div.xpath('./a/text()').extract_first()
            comment = div.xpath('./span[@class="ctt"]')[0]
            content  = comment.xpath('string(.)').extract()[0]
            comment_item['content']= self.ucs(content)
            real_name = div.xpath('./img/@src').extract()
            if len(real_name) > 0:
                comment_item['real_name'] = 1
            else:
                comment_item['real_name'] = 0
            yield comment_item
            #print(comment_item)
        next_href = response.xpath('//body/div[@class="pa"]/form/div/a/@href').extract_first()

        if next_href is not None:
            url = 'https://weibo.cn'+ next_href
            yield Request(url,
                          callback=self.comment_information
                          )


    def redis_push(self, url):
        r = redis.Redis(host='10.1.195.143', port=6379, db=0, password='samVW!$#jh')
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=123456)
        if url.startswith('http'):
            oldUrl = url

        key = hash(url)
        fileName = str(key) + '.jpg'
        newUrl = "http://img.market.maizuo.com/" + str(key) + '.jpg'

        data = {
            'fileName': fileName,
            'oldUrl': oldUrl,
            'newUrl': "http://img.market.maizuo.com/" + fileName,
            'sourceName': "weibo",
        }
        json_data = json.dumps(data)
        r.lpush('WEIBO_IMG', json_data)
        return newUrl

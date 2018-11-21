# -*- coding: utf-8 -*-
import scrapy
import time
import requests
import time
from selenium import webdriver
import re
from WeiBo import  settings
from WeiBo.items import WeiboItem
class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']

    def start_requests(self):
        start_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%97%A0%E5%8F%8C+%E7%94%B5%E5%BD%B1'

        yield scrapy.Request(start_url,callback=self.parse)
    def parse(self, response):
        print(response.text)


        #p = input("请输入要查询的内容：")
        # date_start = str(input("请输入要查询的起始时间："))
        # date_finish = str(input("请输入要查询的终止时间"))
        # year_start = date_start[0:4]
        # month_start =date_start[4:6]
        # day_start = date_start[6:8]
        # year_finish = date_finish[0:4]
        # month_finish = date_finish[4:6]
        # day_finish = date_finish[6:8]
        # param_list=['无双']
        #
        # for p in param_list:
        #     for time in range(1, 17):
        #
        #         if time <10:
        #
        #            start_url = 'https://s.weibo.com/weibo?q={}%20%E7%94%B5%E5%BD%B1&typeall=1&suball=1&timescope=custom:2018-10-0{}-0:2018-10-0{}-23&Refer=SWeibo_box'.format(p,time,time)
        #         else:
        #            start_url='https://s.weibo.com/weibo?q={}%20%E7%94%B5%E5%BD%B1&typeall=1&suball=1&timescope=custom:2018-10-{}-0:2018-10-{}-23&Refer=SWeibo_box'.format(p,time,time)
        #         yield scrapy.Request(start_url,

                                     # headers={
                                     #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'},
                                     # callback=self.parse)
    # def parse(self, response):
    #     # href=response.xpath('//div[@class="c"]/div/a[@class="nk"]/@href')
    #     # print(href)
    #     card_list = response.xpath('//div[@class="card"]')
    #     for card in card_list:
    #         item = WeiboItem()
    #         user_name = card.xpath('.//a/@nick-name').extract_first()
    #         user_href = card.xpath('.//div[@class="content"]//div/div[2]/a/@href').extract_first()
    #         user_href = 'https://' + user_href
    #         leixing = card.xpath('.//div[@class="info"]/div[2]/a/@title').extract_first()
    #         if leixing is None:
    #             leixing = '普通用户'
    #         else:
    #             leixing = leixing
    #         display = card.xpath('.//div[@class="content"]/p/@style').extract_first()
    #         if display is not None:
    #             text = card.xpath('.//div[@class="content"]/p[@style="display: none"]')
    #             text = text[0].xpath('string(.)').extract()[0]
    #             # print(text)
    #         else:
    #
    #             text = card.xpath('.//div[@class="content"]/p[@class="txt"]')
    #             text = text[0].xpath('string(.)').extract()[0]
    #             # print(text)
    #         date = card.xpath('.//div[@class="content"]//p[@class="from"]/a/text()').extract_first()
    #         zhuanfa = card.xpath('./div[@class="card-act"]/ul/li[2]/a/text()').extract_first()
    #         if zhuanfa == "转发 ":
    #             print("没人转发")
    #         else:
    #             print(zhuanfa)
    #
    #         pinglun = card.xpath('./div[@class="card-act"]/ul/li[3]/a/text()').extract_first()
    #         if pinglun == "评论 ":
    #             print("没人评论")
    #         else:
    #             print(pinglun)
    #
    #         dianzan = card.xpath('./div[@class="card-act"]/ul/li[4]/a/em/text()').extract_first()
    #         if dianzan is None:
    #             print("没人点赞")
    #         else:
    #             print(dianzan)
    #         print(user_name)
    #         print(user_href)
    #         print(leixing)
    #         print(text)
    #         print(date)

        # li_list = response.xpath('//div[@class="card"]/div[@class="card-act"]/ul')
        # for li in li_list:
        #     zhuanfa = li.xpath('./li[2]/a/text()').extract_first()
        #     pinglun = li.xpath('./li[3]/a/text()').extract_first()
        #     dianzan = li.xpath('./li[4]/a/em/text()').extract_first()
        #     print(zhuanfa)
        #     print(pinglun)
        #     print(dianzan)
        # content = response.xpath('//div[@class="card"]//div[@class="content"]')

        # for card in content:
        #     times = card.xpath('.//p[@class="from"]/a/text()').extract_first()
        #     display = card.xpath('./p/@style').extract_first()
        #     if display is not None:
        #         text = card.xpath('./p[@style="display: none"]')
        #         text =text[0].xpath('string(.)').extract()[0]
        #         #print(text)
        #     else:
        #
        #         text =  card.xpath('./p[@class="txt"]')
        #         text = text[0].xpath('string(.)').extract()[0]
        #         #print(text)
        #     user_href = card.xpath('.//div/div[2]/a/@href').extract_first()
        #     user_href = 'https://' + user_href


            # chrome_options = webdriver.ChromeOptions()
            # # 使用headless无界面浏览器模式
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            #
            # driver = webdriver.Chrome(chrome_options=chrome_options)
            # driver = webdriver.Chrome()
            # driver.get(user_href)
            # time.sleep(12)
            # a = driver.find_element_by_xpath('//div[@class="pf_username"]/h1')
            #
            # print(a.text)
            # driver.quit()
        #     print(user_href)
        #     yield scrapy.Request(
        #         user_href,
        #         callback=self.page
        #     )
    # def page(self,response):
    #     fensi = response.xpath('//div[@class="pf_username"]/h1[@class="username"]/text()').extract_first()
    #     print(response.text)
    #     url=str(response.headers['Location'])
    #     url = re.findall("b'(.*?)'",url)[0]
    #     print(response.text)'''






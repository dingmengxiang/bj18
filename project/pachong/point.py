#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2018/10/19
# @File   : sellpointspidersvr.py

from tornado.web import RequestHandler
import tornado.ioloop
import requests
from lxml import etree
import re
import pymysql
import hashlib
import time
import redis
import json
#from YoKa import yokaspider
class yoka():
    def __init__(self,keywords):
        self.url_temp = 'http://zhannei.baidu.com/cse/search?q='+keywords+'&p={}&s=2300126470136754598&nsid=1&entry=1'
        self.headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
        self.get_item = 0
    def get_url_list(self):
        url_list=[]
        for i in range(0,2):
            url_list.append(self.url_temp.format(i))
        return url_list
    def parse_url(self,url):
        response = requests.get(url)
        return response.content.decode()
    def get_content_list(self,html_str):
        html =etree.HTML(html_str)
        div_list = html.xpath('//div[@id="results"]/div')
        href_list = []
        for div in div_list:
            # item = {}

            href = div.xpath('.//a/@href')[0]
            # item['href'] = href


            href_list.append(href)
        return href_list
            # print(href)
    def get_content(self,href):
        text = requests.get(href,headers=self.headers)

        html = text.content.decode("gb2312","ignore")
        #print(html)
        #print(html)
        html = etree.HTML(html)
        item = {}

        try:
            item['url'] = href

            title = html.xpath('//div[@class="gLeft"]/h1/text()')[0]
            item['title'] = title
            time =str(html.xpath('//div[@class="time"]/i/text()')[0])
            #print(time)
            item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)',time)[0])
            # div = html.xpath('//div[@class="textCon"]')
            # content1 = etree.tostring(div).decode()
            content =re.findall('<div class="double_quotes">.*?class="publicAccount"',text.content.decode("gb2312","ignore"),re.S)[0]


            is_img = html.xpath('//div[@class="textCon"]//img/@src')
            if len(is_img)>0:
                item['has_img'] = 1
                for img in is_img:
                    newUrl = self.redis_push(img)
                    a = re.findall('(.*)' + str(img) + '(.*)', content, re.S)
                    content = a[0][0] + str(newUrl) + a[0][1]
            else:
                item['has_img'] = 0
            item['content'] = re.sub('提示：', '', content)
            item['content'] = re.sub('<i>图片来源：.*?</i>', '', item['content'])
            item['content'] = re.sub('<a.*?>', '', item['content'])
            item['content'] = re.sub('<i>.*?</i>', '', item['content'])
            item['content'] = re.sub('style=".*?"', '', item['content'])
            # kk = re.findall('.*</p>(.*)', item['content'], re.S)
            # try:
            #     item['content'] = item['content'].replace(kk[0], '')
            # except:
            #     pass

            return item

        except Exception as e :
            #print("网页无法解析:",e)
            return self.again_get(html,item,href)

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
        source = 'YOKA'
        data = {
            'fileName': fileName,
            'oldUrl': oldUrl,
            'newUrl': "http://img.market.maizuo.com/" + fileName,
            'sourceName': source,
        }
        json_data = json.dumps(data)
        r.lpush('IMG_ALI_OSSs', json_data)
        return newUrl
    def save(self,item):

        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="market_spider",
            user="root",
            passwd="root",
            charset='utf8mb4',
            use_unicode=True
        )
        cursor = conn.cursor()

        try:
            h1 = hashlib.md5()



            print(item['url'])
            h1.update(item['url'].encode(encoding='utf-8'))

            hash = h1.hexdigest()

            fetch_time = int(time.time())

            cursor.execute(
                "select id from spider_posts where hash='{0}'".format(hash)
            )
            data = cursor.fetchall()
            print(len(data))
            if len(data) == 0:

                # try:
                cursor.execute('''INSERT INTO spider_posts(url,title,author,content,status,has_img,hash,source,create_time,fetch_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (item['url'], item['title'], '',item['content'], 1, item['has_img'], hash, 'YOKA',
                         item['create_time'], fetch_time))


                # except Exception as e:
                #     print(e)

                print('插入成功')
                self.get_item = self.get_item + 1
                print('本次累计插入%d次'%self.get_item)
                conn.commit()
                conn.close()
            else:
                print('数据已存在')
        except:
            pass
    def again_get(self,html,item,href):
        try:
            text = requests.get(href, headers=self.headers)

            html = text.content.decode("utf8", "ignore")
            # print(html)
            html = etree.HTML(html)
            # try:
            title = html.xpath('//div[@class="conts"]/h1/text()')[0]
            item['title'] = title
            item['url'] = href
            time = html.xpath('//div[@class="time"]/span/text()')[0]

            time = re.findall('发表于：(.*)',time)[0]
            print(item['url'])
            item['create_time'] = ''.join(re.findall('(\d+)-(\d+)-(\d+)', time)[0])
            content =re.findall('<div class="lead">(.*?)<div data-type="appDown_760">',text.content.decode("utf8", "ignore"),re.S)[0]
            item['content'] = content
            is_img = html.xpath('//div[@class="conts"]//img/@_src')
            print(is_img)
            if len(is_img)>0:
                item['has_img'] = 1
                for img in is_img:
                    newUrl = self.redis_push(img)
                    a = re.findall('(.*)' + str(img) + '(.*)', content, re.S)
                    content = a[0][0] + str(newUrl) + a[0][1]
            else:
                item['has_img'] = 0
            item['content'] = re.sub('提示：.*', '', content)
            item['content'] = re.sub('<i>图片来源：.*?</i>', '', item['content'])
            item['content'] = re.sub('<a.*?>', '', item['content'])
            item['content'] = re.sub('<i>.*?</i>', '', item['content'])
            item['content'] = re.sub('style=".*?"', '', item['content'])
            # kk = re.findall('.*</p>(.*)', item['content'], re.S)
            # try:
            #     item['content'] = item['content'].replace(kk[0], '')
            # except:
            #     pass
            #print(item['content'])
            #print(item)
            return item

        except:
            pass

    def run(self):
        url_list = self.get_url_list()

        for url in url_list:
            html_str = self.parse_url(url)
            href_list = self.get_content_list(html_str)
            for href in href_list:
                item = self.get_content(href)
                self.save(item)

class test(RequestHandler):
    # def post(self):
    #     var1=self.get_argument("keyword")
    #     print(var1)
    #     self.write("post Method")
    def get(self):
        #var1 = self.get_argument("keyword")
        global yoka

        self.write("success")
        keywords = self.get_argument('key')
        instance = yoka(keywords)
        instance.run()
        print(instance.get_item)
        self.write("success:%d"%instance.get_item)







# def spider(input):
#     pass

if __name__ == "__main__":

    app = tornado.web.Application([
        (r"/test",test),
        #(r"/yokaspider",yokaspider)


    ])
    app.listen(8610)
    tornado.ioloop.IOLoop.current().start()

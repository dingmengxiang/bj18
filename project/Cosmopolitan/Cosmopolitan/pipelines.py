# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Cosmopolitan import  settings
import hashlib
import time
import logging

class CosmopolitanPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        self.get_item = 0
    def process_item(self, item, spider):
        if spider.name == 'cosmopolitan':
            try:
                h1 = hashlib.md5()
                h1.update(item['url'].encode(encoding='utf-8'))
                hash = h1.hexdigest()
                source = settings.COMPANY_FROM
                fetch_time = int(time.time())
                self.cursor.execute(
                    "select id from spider_posts where hash='{0}'".format(hash)
                )
                # print(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()), '查询')
                data = self.cursor.fetchall()
                if len(data) == 0:
                    self.cursor.execute(
                        '''INSERT INTO spider_posts(url,title,author,content,status,has_img,hash,source,create_time,fetch_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (item['url'], item['title'], '', item['content'], 1, item['has_img'], hash, source,
                         item['create_time'], fetch_time)
                    )
                    print(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()), '插入成功')
                    self.conn.commit()
                    print(item['title'] + '数据插入成功')
                    self.get_item = self.get_item + 1
                    print("本次爬取累计插入成功" + str(self.get_item) + "次")
                else:
                    print('数据已存在')
            except Exception as e:
                print('***************************************')
                print(e)
        else:
            print("爬虫命名错误")

    def close_spider(self, spider):
        self.conn.close()
        logging.info('本次爬取共插入成功' + str(self.get_item) + '次')


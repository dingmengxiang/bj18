# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import logging
import time

import pymysql

from TianYanCha import settings


class TianyanchaPipeline(object):

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
        self.cursor = self.conn.cursor()
        self.get_item = 0
        self.start_time = time.time()

    def process_item(self, item, spider):
        if spider.name == 'tyc':

            url = item['url']
            token = hashlib.md5(url.encode("utf-8")).hexdigest()
            # 判断url是否取过
            sql0 = "SELECT id FROM com_industry where token = '%s' limit 1;" % token
            self.cursor.execute(sql0)
            rows = self.cursor.fetchone()
            # 开始存入数据
            if not rows:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    self.cursor.execute(
                        """INSERT INTO com_industry (name, industry, url, create_time, token, excel_id, mobile) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s) """,
                        (item['name'], item['industry'], item['url'], create_time, token, item['excel_id'], item['mobile'])
                    )
                    self.conn.commit()
                    print("新数据：%s 采集成功" % item['name'])
                except Exception as err:
                    print("插入数据库时错误：")
                    print(err)

                self.get_item = self.get_item + 1
            else:
                print("链接 %s 已经取过, 不再存入" % url)

    def close_spider(self, spider):
        end_time = time.time()
        print("耗时：")
        print(end_time - self.start_time)
        print('本次爬取共采集成功' + str(self.get_item) + '次')
        logging.info('本次爬取共采集成功' + str(self.get_item) + '次')

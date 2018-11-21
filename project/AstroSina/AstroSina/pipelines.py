# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from . import settings
import time
import datetime
class AstrosinaPipeline(object):
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

    def process_item(self, item, spider):
        #self.cursor.execute(''DELET from star''')
        fetch_time = datetime.datetime.now()
        self.cursor.execute(
            "select id from spider_star where constellation='{0}' ".format(item['constellation'])
        )
        # print(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()), '查询')
        data = self.cursor.fetchall()
        #data = self.cursor.fetchall()
        if len(data) == 0:
            self.cursor.execute('''INSERT INTO spider_star (constellation,c_day,health_num,luck_crystal,luck_color,luck_num,noble_con,today_remind,is_do,not_do,create_time,update_time,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                (item['constellation'],fetch_time,item['health_num'],item['luck_crystal'],item['luck_color'],item['luck_num'],item['noble_con'],item['today_remind'],item['is_do'],item['not_do'],fetch_time,fetch_time,1))
        else:
            self.cursor.execute("update spider_star set c_day=\'%s\',health_num=\'%s\',luck_crystal=\'%s\',luck_color=\'%s\',luck_num=\'%s\',noble_con=\'%s\',today_remind=\'%s\',is_do=\'%s\',not_do=\'%s\',create_time=\'%s\',update_time=\'%s\',status=\'%s\' where constellation=\'%s\' " % (fetch_time,item['health_num'],item['luck_crystal'],item['luck_color'],item['luck_num'],item['noble_con'],item['today_remind'],item['is_do'],item['not_do'],fetch_time,fetch_time,1,item['constellation']))
        self.conn.commit()
    def close_spider(self, spider):
        self.conn.close()


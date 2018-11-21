# -*- coding: utf-8 -*-
import pymysql
from . import settings
import hashlib
import time
import logging

import pymysql

class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
           # charset='utf8mb4',
          #  use_unicode=True
        )
        self.cursor = self.conn.cursor()
        self.get_item = 0
    def process_item(self, item, spider):

        if item['name'] == 'data':

            h1 = hashlib.md5()
            h1.update(item['weibo_url'].encode(encoding='utf-8'))
            hash = h1.hexdigest()

            fetch_time = int(time.time())
            self.cursor.execute(
                "select id from weibo_sns where hash='{0}'".format(hash)
            )
            data = self.cursor.fetchall()

            try:
                if len(data) == 0:
                    self.cursor.execute('''INSERT INTO weibo_sns (weibo_url,content,hash,repost_num,like_num,comment_num,_id,fetch_time,create_time,keywords,created_from,img_url,img_href) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                        (item["weibo_url"], item["content"],hash,item['repost_num'],item['like_num'],item['comment_num'],item['_id'],fetch_time,item['create_time'],item['keyword'],item['created_from'],item['img_url'],item['img_href']))
                    self.conn.commit()
                    print(item['keyword'] + '数据插入成功')
                    self.get_item = self.get_item + 1
                    print("本次爬取累计插入成功" + str(self.get_item) + "次")
                else:
                    print(item['keyword'] + "数据已存在")
            except Exception as e:
                print('***************************************')
                print(e)
        elif item['name'] == 'information':
            try:
                h1 = hashlib.md5()
                h1.update(item['_id'].encode(encoding='utf-8'))
                hash = h1.hexdigest()

                fetch_time = int(time.time())
                self.cursor.execute(
                    "select id from weibo_user_info where hash='{0}'".format(hash)
                )
                data = self.cursor.fetchall()
                if len(data) == 0:
                    # print('**************')
                    # print(item['brief_introduction'])
                    # print(item['city'])
                    try:
                        self.cursor.execute('''INSERT INTO weibo_user_info (_id,nick_name,hash,gender,province,city,brief_introduction,birthday,tweets_num,fans_num,follows_num,sex_orientation,sentiment,vip_level,authentication,fetch_time,is_v,label,school,head_img) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                            (item["_id"],item["nick_name"],hash,item['gender'],
                                             item['province'],item['city'],item['brief_introduction'],
                                             item['birthday'], item['tweets_num'],
                                             item['fans_num'],item['follows_num'],
                                             item['sex_orientation'],item['sentiment'],
                                             item['vip_level'],item['authentication'],
                                             fetch_time,item['is_v'],item['label'],
                                             item['school'],item['head_img']
                                             ))
                    except Exception as e:
                        print(e)
                    self.conn.commit()
                    print(item['nick_name'] + '数据插入成功')
                    self.get_item = self.get_item + 1
                    print("本次爬取累计插入成功" + str(self.get_item) + "次")
                else:
                    print(item['nick_name'] + "数据已存在")
            except Exception as e:
                print('***************************************')
                print(e)
        else:
            h1 = hashlib.md5()
            h1.update(item['weibo_url'].encode(encoding='utf-8'))
            hash = h1.hexdigest()

            self.cursor.execute('''INSERT INTO comment (_id,name,content,weibo_url,commenter_url,real_name,hash) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                (item["_id"],item["name"],item["content"] ,item['weibo_url'],item['commenter_url'],item['real_name'],hash))
            self.conn.commit()
            print(item['name'] + '数据插入成功')
            self.get_item = self.get_item + 1
            print("本次爬取累计插入成功" + str(self.get_item) + "次")


    def close_spider(self, spider):
        self.conn.close()
        logging.info('本次爬取共插入成功' + str(self.get_item) + '次')

# class MongoDBPipeline(object):
#     def __init__(self):
#         client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
#         db = client[DB_NAME]
#         self.Information = db["Information"]
#         self.Tweets = db["Tweets"]
#         self.Comments = db["Comments"]
#         self.Relationships = db["Relationships"]
#
#     def process_item(self, item, spider):
#         """ 判断item的类型，并作相应的处理，再入数据库 """
#         if isinstance(item, RelationshipsItem):
#             self.insert_item(self.Relationships, item)
#         elif isinstance(item, TweetsItem):
#             self.insert_item(self.Tweets, item)
#         elif isinstance(item, InformationItem):
#             self.insert_item(self.Information, item)
#         elif isinstance(item, CommentItem):
#             self.insert_item(self.Comments, item)
#         return item
#
#     @staticmethod
#     def insert_item(collection, item):
#         try:
#             collection.insert(dict(item))
#         except DuplicateKeyError:
#             """
#             说明有重复数据
#             """
#             pass

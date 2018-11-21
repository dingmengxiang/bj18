# encoding: utf-8
import random


import pymysql



class CookieMiddleware(object):
    """
    每次请求都随机从账号池中选择一个账号去访问
    """
    # def process_request(self, request, spider):
    #     cookie_list = ['_T_WM=1ed1db312f85efb881a3a7a8f8cbf08b; SUB=_2A252zQ8iDeRhGeBJ6loY9SjPzD-IHXVSMZFqrDV6PUJbkdAKLRTHkW1NRk11VpOqTTG5HUfjkaM3y1In_SGJRfD4; SUHB=0ebtwKN_dIEkPA; SCF=Aj5S6G1aQg-Qu2AxYwFfSs-QXBoqbK4mJNMLLs8y7iDRioYc5x6dsFWdd9_CWUuWzJ50fXTZf6slAtRbgTYZmek.; SSOLoginState=1539932018'
    #
    #     ]
    #     cookie = random.choice(cookie_list)
    #     request.headers.setdefault('cookie',cookie)
    def __init__(self):
        self.client = pymysql.connect(host='gz-cdb-l4r5h3m3.sql.tencentcdb.com',port=61928,user='root',passwd='samVW!$#jh',db='market_spider',charset='utf8',use_unicode=True)
        self.cursor = self.client.cursor()
    def process_request(self,request,spider):
        self.cursor.execute(
            "select id from weibo_user_cookie where status='success'"
        )
        data = self.cursor.fetchall()
        if len(data) == 0:
            print("当前账号池为空")
        else:
            random_index = random.randint(0,len(data)-1)
            all_data=self.cursor.execute("select * from weibo_user_cookie where status='success'")
            all_data = self.cursor.fetchall()
            random_cookie = all_data[random_index][3]
            request.headers.setdefault('Cookie', random_cookie)
            request.meta ['account'] = all_data[random_index]






    # def __init__(self):
    #     client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
    #     self.account_collection = client[DB_NAME]['account']
    #
    # def process_request(self, request, spider):
    #     all_count = self.account_collection.find({'status': 'success'}).count()
    #     if all_count == 0:
    #         raise Exception('当前账号池为空')
    #     random_index = random.randint(0, all_count - 1)
    #     random_account = self.account_collection.find({'status': 'success'})[random_index]
    #     request.headers.setdefault('Cookie', random_account['cookie'])
    #     request.meta['account'] = random_account


class RedirectMiddleware(object):
    """
    检测账号是否正常
    302 / 403,说明账号cookie失效/账号被封，状态标记为error
    418,偶尔产生,需要再次请求
    """

    def __init__(self):
        self.client = pymysql.connect(host='gz-cdb-l4r5h3m3.sql.tencentcdb.com',port=61928,user='root',passwd='samVW!$#jh',db='market_spider',charset='utf8',use_unicode=True)
        self.cursor = self.client.cursor()

    def process_response(self, request, response, spider):
        http_code = response.status

        if http_code == 302 or http_code == 403:

            self.cursor.execute("update weibo_user_cookie set status='error' where username='{}'".format(request.meta['account'][1]))
            self.client.commit()
            return request
        elif http_code == 418:
            return request
        else:
            return response

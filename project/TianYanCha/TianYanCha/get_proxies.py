# 多线程代理（普通和redis多数无效）
# import json
# import re
# import time
# from queue import Queue
# import threading
#
# import redis
# import requests
#
#
# class Proxies(object):
#     def __init__(self):
#         self.ip_set = set()
#         self.que_proxy = Queue()
#
#     # 启动线程
#     def get_begin(self):
#         threads = []
#         t1 = threading.Thread(target=self.get_proxies_1)
#         threads.append(t1)
#         # t2 = threading.Thread(target=self.get_proxies_2)
#         # threads.append(t2)
#         # t3 = threading.Thread(target=self.get_proxies_3)
#         # threads.append(t3)
#
#         for t in threads:
#             t.setDaemon(True)
#             t.start()
#
#     # 代理3
#     def get_proxies_3(self):
#         myredis = redis.Redis(host='10.1.195.143', port=6379, db=0, password='samVW!$#jh')
#         while 1:
#             ip = myredis.get('ip')
#             ip = ip.decode()
#             if ip != '':
#                 if ip not in self.ip_set:
#                     self.ip_set.add(ip)
#                     proxies = {
#                         "http": "http://" + ip,
#                         "https": "https://" + ip
#                     }
#                     try:
#                         if requests.get('http://www.baidu.com/', proxies=proxies, timeout=2).status_code == 200:
#                             print("获取到redis代理：%s" % proxies)
#                             self.que_proxy.put(proxies)
#                     except:
#                         pass
#             else:
#                 print("redis未获取到ip，休眠5秒")
#                 time.sleep(5)
#
#     # 代理2
#     def get_proxies_2(self):
#         while 1:
#             time.sleep(1)
#             old_proxies = []
#
#             # 获取
#             jsonstr = requests.get('http://api.ip.data5u.com/api/get.shtml?order=cab22ba3d2f7000f87783c3ab3499e97&num=100&area=%E9%9D%9E%E4%B8%AD%E5%9B%BD&carrier=0&protocol=0&an1=1&sp1=1&sp2=2&sort=1&system=1&distinct=0&rettype=0&seprator=%0A', timeout=2).text
#             if "data" in jsonstr:
#                 jsontrees = json.loads(jsonstr)
#                 for data in jsontrees["data"]:
#                     ip = str(data["ip"]) + ":" + str(data["port"])
#                     old_proxies.append(ip)
#
#                 # 验证
#                 for ip in old_proxies:
#                     proxies = {
#                         'https': "https://" + str(ip),
#                         'http': "http://" + str(ip)
#                     }
#                     if ip not in self.ip_set:
#                         self.ip_set.add(ip)
#                         try:
#                             if requests.get('http://www.baidu.com/', proxies=proxies, timeout=2).status_code == 200:
#                                 print("获取到普通代理：%s" % proxies)
#                                 self.que_proxy.put(proxies)
#                         except:
#                             pass
#             else:
#                 print("普通代理未获取到IP，休眠3秒")
#                 time.sleep(3)
#
#     # 代理1
#     def get_proxies_1(self):
#         while 1:
#             text = requests.get('http://api.ip.data5u.com/dynamic/get.html?order=cab22ba3d2f7000f87783c3ab3499e97&random=true&sep=3').text
#             try:
#                 ip = re.findall('(\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3}:\d{4,5})', text)[0]
#             except:
#                 ip = ''
#             if ip != '':
#                 proxies = {
#                     "http": "http://" + ip,
#                     "https": "https://" + ip
#                 }
#                 if ip not in self.ip_set:
#                     self.ip_set.add(ip)
#                     self.que_proxy.put(proxies)
#             else:
#                 print("爬虫接口未获取到IP，休眠3秒")
#                 time.sleep(3)
#
#     # 从队列获取有效代理
#     def get_useful_proxies(self):
#         if not self.que_proxy.empty():
#             proxies = self.que_proxy.get()
#             # print("获取到代理：%s" % proxies)
#             return proxies
#         else:
#             print("queue empty. please wait for 2 second")
#             time.sleep(2)

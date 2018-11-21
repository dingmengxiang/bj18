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
r

class test(RequestHandler):
    # def post(self):
    #     var1=self.get_argument("keyword")
    #     print(var1)
    #     self.write("post Method")
    def get(self):
        var1 = self.get_argument("keyword")

        yoka = yoka(var1)
        yoka.run()
        self.write("get Method")






# def spider(input):
#     pass

if __name__ == "__main__":

    app = tornado.web.Application([
        (r"/test",test)


    ])
    app.listen(8620)
    tornado.ioloop.IOLoop.current().start()

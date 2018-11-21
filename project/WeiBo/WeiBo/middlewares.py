# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random
import time
import redis
import requests
import re


class WeiboSpiderMiddleware(object):
    def __init__(self, ip=''):
        self.ip = ip
        self.start_time=int(time.time())

    def process_request(self, request, spider):
        wait_time=time.time()-self.start_time
        if wait_time>5:
            self.start_time=int(time.time())
            self.ip=self.get_ip()
        if self.ip!='':
            print("获取到 ip:" + self.ip)
            request.meta["proxy"] = "http://" +self.ip
        else:
            print("未获取到ip，休眠5秒")
            time.sleep(5)

    def get_ip(self):
        myredis = redis.Redis(host='10.1.195.143', port=6379, db=0, password='samVW!$#jh')
        try:
            ip = myredis.get("ip")
            ip = ip.decode("utf-8")
            return ip
        except:
            return ''

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
# class CookieMiddleware(object):
#     def __init__(self):
#         self.list_cookie = ['SINAGLOBAL=4478965905471.064.1536734492956; wvr=6; login_sid_t=c990ff4d1a7a4ebf668af4daec9f6363; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; UOR=finance.ifeng.com,widget.weibo.com,www.baidu.com; Apache=7516744211560.431.1539822976328; ULV=1539822976341:7:5:4:7516744211560.431.1539822976328:1539738200465; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFbYnOkrCi0MEWUfulpss3B5JpX5K2hUgL.FoqNe0.peheNShz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM4SoM0SK2feoeR; ALF=1571358991; SSOLoginState=1539822992; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHAut7K_II6nUsABDhhxD-BhnpAe1F61cEgNFOfARyz7A.; SUB=_2A252w6XADeRhGeBJ6FsQ8C3Lzz6IHXVVuJAIrDV8PUNbmtBeLRbQkW9NRi7p5I1wQMuUn2PXiOyeh0qel-xuhO05; SUHB=0C1CuochMijcvg; un=17337735053; WBStorage=e8781eb7dee3fd7f|undefined','SINAGLOBAL=7276625595936.525.1537165523829; UOR=enrz.com,widget.weibo.com,www.baidu.com; un=15209474712; wvr=6; SCF=Ajg3_3GFQV6zAijOVXaz9wsRH5OdN1xSYccPrLXyVvhguRzFiLgNj7j1Cc3o20XVcEKqilaQZ2J7hq-xezBTgzg.; SUB=_2A252w5k_DeRhGeBJ6loY9SjPzD-IHXVVuI33rDV8PUNbmtBeLRjZkW9NRk11Vo337_8Fg2q-E-cMyo4pcRtDFbuR; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhoQXbfcXC6aXAmFChuzDUu5JpX5KzhUgL.FoqNeKn4SKq0S0e2dJLoI7yXdcUaeozEentt; SUHB=0TPVYifMInPx0e; _s_tentry=login.sina.com.cn; Apache=8000520300187.055.1539828085411; ULV=1539828085439:8:6:5:8000520300187.055.1539828085411:1539741999074','SINAGLOBAL=7276625595936.525.1537165523829; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; YF-V5-G0=694581d81c495bd4b6d62b3ba4f9f1c8; YF-Page-G0=ed0857c4c190a2e149fc966e43aaf725; wb_view_log_6718956373=1440*9001; _s_tentry=login.sina.com.cn; Apache=8000520300187.055.1539828085411; ULV=1539828085439:8:6:5:8000520300187.055.1539828085411:1539741999074; WBtopGlobal_register_version=030d061db77a53e5; login_sid_t=ed73c3d47319c7e0e0b31587ccafd446; cross_origin_proto=SSL; WBStorage=e8781eb7dee3fd7f|undefined; UOR=enrz.com,widget.weibo.com,login.sina.com.cn; wb_view_log=1440*9001; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF-ycpUlRakrVKK5GmQ7pE55JpX5K2hUgL.FoqNeKn4SK-4e0-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcS02R1K-f1Kef; ALF=1571365425; SSOLoginState=1539829425; SCF=Ajg3_3GFQV6zAijOVXaz9wsRH5OdN1xSYccPrLXyVvhgw4dMzORYeDC7tSOMYPViObtQNCxG3l8fasgNedR9q9U.; SUB=_2A252w57iDeRhGeBJ6loY9SvFyDmIHXVVuPcqrDV8PUNbmtBeLXTckW9NRk10ux-aQeTaz_dff5tLpnc2C-Buu3cJ; SUHB=0S7CN12OougT2s; un=17006587164; wvr=6; wb_view_log_6718955935=1440*9001','SINAGLOBAL=7276625595936.525.1537165523829; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; YF-V5-G0=694581d81c495bd4b6d62b3ba4f9f1c8; YF-Page-G0=ed0857c4c190a2e149fc966e43aaf725; wb_view_log_6718956373=1440*9001; _s_tentry=login.sina.com.cn; Apache=8000520300187.055.1539828085411; ULV=1539828085439:8:6:5:8000520300187.055.1539828085411:1539741999074; WBtopGlobal_register_version=030d061db77a53e5; login_sid_t=ed73c3d47319c7e0e0b31587ccafd446; cross_origin_proto=SSL; WBStorage=e8781eb7dee3fd7f|undefined; UOR=enrz.com,widget.weibo.com,login.sina.com.cn; wb_view_log=1440*9001; wb_view_log_6718955935=1440*9001; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFdJUnzE1Jhz_3r8dBruTHL5JpX5K2hUgL.FoqNeKn7eoeESoz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcS02Rehz0eoqE; ALF=1571365576; SSOLoginState=1539829576; SCF=Ajg3_3GFQV6zAijOVXaz9wsRH5OdN1xSYccPrLXyVvhgL3ZIzj2udIfksuSDTAEaTprOOM17uYOK0O0lOGq2lXY.; SUB=_2A252w58ZDeRhGeBJ6loR8i3OzT6IHXVVuPfRrDV8PUNbmtBeLXLekW9NRk10qE1gMe3XGLx11iWBaB_wpXg-16m3; SUHB=0z1AmBaOeQCXXR; un=15092534233; wvr=6; wb_view_log_6718023262=1440*9001','SINAGLOBAL=7276625595936.525.1537165523829; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; YF-V5-G0=694581d81c495bd4b6d62b3ba4f9f1c8; YF-Page-G0=ed0857c4c190a2e149fc966e43aaf725; wb_view_log_6718956373=1440*9001; _s_tentry=login.sina.com.cn; Apache=8000520300187.055.1539828085411; ULV=1539828085439:8:6:5:8000520300187.055.1539828085411:1539741999074; WBtopGlobal_register_version=030d061db77a53e5; login_sid_t=ed73c3d47319c7e0e0b31587ccafd446; cross_origin_proto=SSL; UOR=enrz.com,widget.weibo.com,login.sina.com.cn; wb_view_log=1440*9001; wb_view_log_6718955935=1440*9001; wb_view_log_6718023262=1440*9001; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGwFKTw7cNWVmgbZEEX_0s5JpX5K2hUgL.FoqNeKn7eoeEe0q2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcS02Rehz0eoec; SSOLoginState=1539829851; ALF=1571365879; SCF=Ajg3_3GFQV6zAijOVXaz9wsRH5OdN1xSYccPrLXyVvhg7Ka7h_3ITeUQaIBJ_GM02apjQZB9yDx77E0dPJOdoLg.; SUB=_2A252w4ApDeRhGeBJ6loR8i3OyDqIHXVVuPbhrDV8PUNbmtBeLW_QkW9NRk10qqHyEuffwYPYiy7ba7DyhAYJlr37; SUHB=0qj0qfonzhT3cq; un=15634112509; wvr=6; wb_view_log_6718023236=1440*9001']
#
#     def process_request(self, request, spider):
#         cookie = random.choice(self.list_cookie)
#         request.headers.setdefault('Cookie', cookie)
class CookieMiddleware():
    def process_request(self, request, spider):
        # cookie_list = ['SINAGLOBAL=4478965905471.064.1536734492956; wvr=6; wb_timefeed_6739103742=1; un=17337735053; YF-Page-G0=140ad66ad7317901fc818d7fd7743564; _s_tentry=www.baidu.com; UOR=finance.ifeng.com,widget.weibo.com,www.baidu.com; Apache=6325719161440.79.1539912604484; ULV=1539912604525:9:7:6:6325719161440.79.1539912604484:1539910251404; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; WBtopGlobal_register_version=030d061db77a53e5; login_sid_t=68d31c7f66a025732c8e978475919e4b; cross_origin_proto=SSL; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; TC-V5-G0=634dc3e071d0bfd86d751caf174d764e; wb_view_log=1440*9001; YF-V5-G0=8d795ebe002ad1309b7c59a48532ef7d; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHbOAH3aELzEOAgmG8WdKJNKVkvsmX_6X4U-0qCJUrzBY.; SUB=_2A252zUrJDeRhGeBJ6FsQ8C3Lzz6IHXVVuzsBrDV8PUNbmtBeLU_SkW9NRi7p5JHgkeHedNUO2S1x6012c7oxvPc-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFbYnOkrCi0MEWUfulpss3B5JpX5K2hUgL.FoqNe0.peheNShz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM4SoM0SK2feoeR; SUHB=0YhROFv9csGbue; ALF=1540519194; SSOLoginState=1539914394; wb_view_log_6739103742=1440*9001','SINAGLOBAL=4478965905471.064.1536734492956; wb_timefeed_6739103742=1; YF-Page-G0=140ad66ad7317901fc818d7fd7743564; _s_tentry=www.baidu.com; Apache=6325719161440.79.1539912604484; ULV=1539912604525:9:7:6:6325719161440.79.1539912604484:1539910251404; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; WBtopGlobal_register_version=030d061db77a53e5; login_sid_t=68d31c7f66a025732c8e978475919e4b; cross_origin_proto=SSL; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; TC-V5-G0=634dc3e071d0bfd86d751caf174d764e; wb_view_log=1440*9001; YF-V5-G0=8d795ebe002ad1309b7c59a48532ef7d; wb_view_log_6739103742=1440*9001; WBStorage=e8781eb7dee3fd7f|undefined; UOR=finance.ifeng.com,widget.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhoQXbfcXC6aXAmFChuzDUu5JpX5K2hUgL.FoqNeKn4SKq0S0e2dJLoI7yXdcUaeozEentt; ALF=1571458698; SSOLoginState=1539922698; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHzk-6dQjYYFbTG1sol48uw6Ad4lFl1EUJY48b8qFQamI.; SUB=_2A252zStdDeRhGeBJ6loY9SjPzD-IHXVVuxuVrDV8PUNbmtBeLXHRkW9NRk11Vnw_tVSI3wzsAR1nt8Z9_UpBzBwF; SUHB=0d4-abU6zb7brK; un=15209474712; wvr=6; wb_view_log_6718956373=1440*9001','SINAGLOBAL=4478965905471.064.1536734492956; _s_tentry=www.baidu.com; Apache=6325719161440.79.1539912604484; ULV=1539912604525:9:7:6:6325719161440.79.1539912604484:1539910251404; login_sid_t=68d31c7f66a025732c8e978475919e4b; cross_origin_proto=SSL; UOR=finance.ifeng.com,widget.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF-ycpUlRakrVKK5GmQ7pE55JpX5K2hUgL.FoqNeKn4SK-4e0-2dJLoI05LxKML1heLBKqLxKML1heLBKqLxKML1heLBKqLxK-LBK-LB.BLxKML1heLBKq7eK-t; ALF=1571458808; SSOLoginState=1539922809; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjH5LIy5YGGREG8SlMVfQWwrhLZ0fXoNJIUfpV786C2cII.; SUB=_2A252zSspDeRhGeBJ6loY9SvFyDmIHXVVuxvhrDV8PUNbmtBeLUXekW9NRk10u5dq4wCWGunKRZqzSySJf1KYd_tY; SUHB=0JvgEbUmwcSJHX; un=17006587164; YF-Page-G0=b9004652c3bb1711215bacc0d9b6f2b5; wb_view_log_6718955935=1440*9001','SINAGLOBAL=4478965905471.064.1536734492956; wb_timefeed_6739103742=1; YF-Page-G0=140ad66ad7317901fc818d7fd7743564; _s_tentry=www.baidu.com; Apache=6325719161440.79.1539912604484; ULV=1539912604525:9:7:6:6325719161440.79.1539912604484:1539910251404; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; WBtopGlobal_register_version=030d061db77a53e5; login_sid_t=68d31c7f66a025732c8e978475919e4b; cross_origin_proto=SSL; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; TC-V5-G0=634dc3e071d0bfd86d751caf174d764e; wb_view_log=1440*9001; YF-V5-G0=8d795ebe002ad1309b7c59a48532ef7d; wb_view_log_6739103742=1440*9001; WBStorage=e8781eb7dee3fd7f|undefined; UOR=finance.ifeng.com,widget.weibo.com,login.sina.com.cn; wb_view_log_6718956373=1440*9001; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFdJUnzE1Jhz_3r8dBruTHL5JpX5K2hUgL.FoqNeKn7eoeESoz2dJLoI0YLxK-LBKBLBKMLxKnL1-zL12zLxKMLBoeL1K-LxK-LBK-LB.BLxK-L1K2LBozLxK-L1K2LBozLxK-L1K2LBozt; ALF=1571458887; SSOLoginState=1539922888; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHDvbLQDFzGkP2We0tbbg6euEGGL7SCYGpwpJlbx25cgk.; SUB=_2A252zSuYDeRhGeBJ6loR8i3OzT6IHXVVuxpQrDV8PUNbmtBeLXHRkW9NRk10qJAXHAw4iZD16__GpPcQQjabUKAM; SUHB=0HTh3GEceYEd8J; un=15092534233; wvr=6; wb_view_log_6718023262=1440*9001','SINAGLOBAL=4478965905471.064.1536734492956; _s_tentry=www.baidu.com; Apache=6325719161440.79.1539912604484; ULV=1539912604525:9:7:6:6325719161440.79.1539912604484:1539910251404; login_sid_t=68d31c7f66a025732c8e978475919e4b; cross_origin_proto=SSL; UOR=finance.ifeng.com,widget.weibo.com,login.sina.com.cn; YF-Page-G0=b9004652c3bb1711215bacc0d9b6f2b5; wb_view_log_6718955935=1440*9001; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGwFKTw7cNWVmgbZEEX_0s5JpX5K2hUgL.FoqNeKn7eoeEe0q2dJLoIE5LxK.L1KnLB.qLxKqL1KqLB-qLxK.LBK2LB.9.Mcx0qBtt; ALF=1571458991; SSOLoginState=1539922992; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHTrQJtNIEZUsHPW12OLnSU9XUYy0yD1WE1hxjaxpKSQ4.; SUB=_2A252zSxgDeRhGeBJ6loR8i3OyDqIHXVVuxqorDV8PUNbmtBeLW_VkW9NRk10qooMKll2bfkS5Ynr1_WwGZWY-jVC; SUHB=0z1AmBaOXLzoWm; un=15634112509; wb_view_log_6718023236=1440*9001'
        #
        # ]
        cookie_list = ['_T_WM=414d2aac6c20dbbe3b8d1a0df2462c7c; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHg_LLU7QqKYOxNeflnxqGUcJi4HQN8AHdnJnh92oEjBY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGwFKTw7cNWVmgbZEEX_0s5JpX5K-hUgL.FoqNeKn7eoeEe0q2dJLoIE5LxK.L1KnLB.qLxKqL1KqLB-qLxK.LBK2LB.9.Mcx0qBtt; MLOGIN=1; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; SUB=_2A252zfoIDeRhGeBP6lcX9CzLwzuIHXVSMYZArDV6PUJbkdAKLVjXkW1NRZQT4z4oyeZUojhlxUbB_XTu6SjsIFNu; SUHB=0gHizexxnXOuK9; SSOLoginState=1539934808; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D10760320623770']
        cookie = random.choice(cookie_list)
        request.headers.setdefault('cookie',cookie)



class UserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        # 这句话用于随机选择user-agent
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    user_agent_list = [
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
        'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    ]


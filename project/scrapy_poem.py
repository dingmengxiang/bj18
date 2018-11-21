import tornado.web
import json
import redis
import random
import hashlib
from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from  selenium.webdriver.chrome.options import Options
import  time
class  Getpoem(tornado.web.RequestHandler):
    def post(self):
        result='True'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        try:
            resident=['优'  ,'能' ,'健' ,'勤', '好'  ,'善' ,'智' ,'富' ,'专' ,'乐','赞','秀','福','佳','赏','情','兴','和','诚','助','感','责','高','神','顺','心','信','运','行','千','惊','金','往','年']
            print('-------------------' + time.strftime('%Y-%m-%d %H:%M:%S') + '-------------------')
            start_time = time.time()
            r = redis.Redis(host='127.0.0.1', port=6379)
            print(self.request.body.decode())
            #r = redis.Redis(host='r-bp137ca4ff632814.redis.rds.aliyuncs.com', port=6379, db=0, password='samVW!$#jh')
            data = json.loads(self.request.body.decode('utf-8'))
            name_key=str(data['name'])
            key=hashlib.md5(name_key.encode('utf-8')).hexdigest()
            print('key:',key)
            print(time.strftime('%Y%m%d %H:%M:%S')+'开始检测是否存在:',key)
            test_start_time = time.time()
            d = r.get(key)

            print(str(time.strftime('%Y%m%d %H:%M:%S')) + '检测完成，耗时：', str(time.time() - test_start_time))
            if d != None:
                 result='藏头诗已存在'
                 print(d.decode('utf-8'))
            else:
                d=str(name_key)
                print(d)
                if len(d)==3:
                   key_words=d+str(random.sample(resident,1)[0])
                elif len(d)==4:
                    key_words=d
                else:
                    word=random.sample(resident,2)
                    key_words=d+str(word[0])+str(word[1])
                print(str(time.strftime('%Y%m%d %H:%M:%S')) + '开始获取用诗词')
                get_data_start_time = time.time()
                browser.get('http://www.shicimingju.com/cangtoushi/index.html')
                input_content=browser.find_element_by_xpath("//div[@class='layui-form-item']//input[@class='layui-input']")
                input_content.send_keys(key_words)
                input_content.send_keys(Keys.ENTER)
                time.sleep(1)
                content_list=browser.find_elements_by_xpath("//div[@class='cangtoushi-item']")
                for i in range(len(content_list)):
                    content_list[i]=content_list[i].text
                #print(content_list)
                i=len(content_list)
                data = str(content_list[random.randint(0,i)]).encode('utf-8').decode('utf-8')
                data=data.encode('utf-8')
                if len(data) == 0:
                    print(str(time.strftime('%Y%m%d %H:%M:%S')) + '获取失败')
                    result = '获取不到诗词'
                else:
                    print(str(time.strftime('%Y%m%d %H:%M:%S')) + '获取完成，耗时：' + str(time.time() - get_data_start_time))

                    print(str(time.strftime('%Y%m%d %H:%M:%S')) + '开始上传诗词')
                    push_user_start_time=time.time()
                    r.set(key,data)
                    r.expire(key, 43200)
                    print(str(time.strftime('%Y%m%d %H:%M:%S')) + '上传完成，耗时：',str(time.time() - push_user_start_time))
                    result = '上传成功'
                    browser.close()
        except Exception as e:
            raise (e)
        finally:
            print('ending:', time.strftime('%Y-%m-%d %H:%M:%S'))
            print('cost', str(time.time() - start_time))

            print(result)




application = tornado.web.Application([(r"/Getpoem", Getpoem),
])

if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
    tornado.options.parse_command_line()

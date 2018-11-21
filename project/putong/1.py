import time
from selenium import webdriver
import re
import time
from openpyxl import Workbook
import requests
from selenium import webdriver


#实例化一个浏览器
driver = webdriver.Chrome()

#设置窗口大小
#driver.set_window_size(1920,1000)
#最大化窗口
#driver.maximize_window()

#发送请求
# list=['sz000509', 'sh600766']
# for i in list:
#     time.sleep(10)
#     driver = webdriver.Chrome()
#     url='http://finance.sina.com.cn/realstock/company/{}/nc.shtml'.format(i)
#     print(url)
#     driver.get(url)
driver.get('http://finance.sina.com.cn/realstock/company/sh600766/nc.shtml')


#进行页面截屏
#driver.save_screenshot("./baidu.png")


#元素定位的方法
# i=input('请输入内容：')
# print(i)
# driver.find_elements_by_xpath('//input[@autocomplete="off"]')[1].send_keys(str(i))
# driver.find_elements_by_class_name("layui-btn")[0].click()
# a=driver.page_source
#
# a=''.join(re.findall('<div class="cangtoushi-item">(.*?)</div>',a,re.S))
# print('输出的内容是：%s'%a)
# time.sleep(3)
# driver.quit()
#退出浏览器
a=driver.find_elements_by_xpath('//div[@id="MRFlow"]//tbody/tr[2]/td')
b=driver.find_elements_by_xpath('//div[@id="MRFlow"]//tbody/tr[3]/td')
c=driver.find_elements_by_xpath('//div[@id="FLFlow"]//tbody/tr[2]/td')
d=driver.find_elements_by_xpath('//div[@id="FLFlow"]//tbody/tr[3]/td')
e=driver.find_elements_by_xpath('//div[@id="FLFlow"]//tbody/tr[4]/td')
g = driver.find_elements_by_xpath('//h1[@id="stockName"]')
f=g+a+b+c+d+e
data = []
for n in f:
 data.append(n.text)
print(data)
try:
    wb = Workbook()
    ws = wb.active
    ws.append([ '代码','名称','最新价','今日涨跌幅','净额(主力)','净占比(主力)','净额(超大单)','净占比(超大单)','净额(大单)','净占比(大单)','净额(中单)','净占比(中单)','净额(小单)','净占比(小单)','时间'])
    line = data
    ws.append(line)  # 将数据以行的形式添加到xlsx中

    wb.save('e:\\20181014.xlsx')
except Exception as result:
   print("捕获到异常:%s"%result)
time.sleep(3)
driver.quit()
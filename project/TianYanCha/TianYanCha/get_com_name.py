import time
from queue import Queue
import re

import xlrd


class ComInfo(object):
    def __init__(self):
        self.que_com = Queue()
        # self.put_info()

    # 工作簿名称入队
    def put_info(self):
        # 确定文件
        file_path = 'namelist1.xlsx'
        # 打开工作簿
        book = xlrd.open_workbook(file_path)
        # 获取第一张工作表
        sheet = book.sheet_by_index(0)

        start = 1000  # 开始的行
        end = 2000  # 结束的行

        # # 测试
        # start = 440013
        # end = 440023

        # 遍历想要的行数
        for x in range(start, end+1):
            # 取出每一行的数据
            row = sheet.row_values(x)
            company_info = str(row[2])

            # 如果公司名存在，取出数据插入队列
            if company_info:
                if "公司名称" in company_info:
                    company_info = company_info[5:]
                # 取出每行的前三列单元格数据
                try:
                    id = int(row[0])
                    mobile = int(row[1])
                    if '|' not in company_info:
                        if "company" not in company_info:
                            company_info = company_info.replace(' ', '')
                            company = re.findall("[\u4e00-\u9fa5]+[公司|厂|部]+", company_info)
                            if company:
                                if company[0] in ["有限公司", "厂", "部"]:
                                    print("抓到")
                                    print(company)
                                    print(company_info)
                                    company = re.findall("[\u4e00-\u9fa5]+（[\u4e00-\u9fa5]+）[有限公司|厂|部]+", company_info)
                                self.que_com.put({company[0]: [id, mobile]})
                except Exception as err:
                    print("从Excel获取公司信息出错")
                    print(err)

    # 从队列获取公司信息
    def get_com_info(self):
        if not self.que_com.empty():
            com_info = self.que_com.get()
            return com_info
        else:
            print("queue empty. please wait for 1 second")
            time.sleep(1)

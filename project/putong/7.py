import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='market_spider', charset='utf8')
cursor = conn.cursor()
cursor.execute("select * from spider_star")
# data=cursor.fetchone()

#data=data[0]
# print(data)
data1 = cursor.fetchmany()
print(data1)
# data2 = cursor.fetchall()
# print(data2)
cursor.close()
conn.commit()
conn.close()
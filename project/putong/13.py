import pymysql
import re
conn=pymysql.connect(host = 'rm-bp1163rl4802767s8.mysql.rds.aliyuncs.com',db='market_spider',user='sam',passwd='samVW!$#jh')
cursor = conn.cursor()
cursor.execute("select movie_name from movie_info where show_time like '2018%中国大陆%'")
names = str(cursor.fetchall())
name = re.findall("\('(.*?)',\)",names)
print(len(name))
print(name)
# for n in name:
#     print(n)
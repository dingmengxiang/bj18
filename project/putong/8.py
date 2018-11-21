import re
from urllib.parse import unquote
url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%97%A0%E5%8F%8C+%E7%94%B5%E5%BD%B1&advancedfilter=1&starttime=20181001&endtime=20181002&sort=time&page=57'
new_url = unquote(url)
a=re.findall('keyword=(.*?)&',new_url)[0]
print(type(a))
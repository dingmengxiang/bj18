import re
a = 'https://weibo.cn/comment/GDk87fN4F?uid=1765971192&rl=1'
uid = re.findall('uid=(.*?)&',a)[0]
string = re.findall('comment/(.*?)\?',a)[0]
weibo_url = 'https://weibo.cn/'+uid+'/'+string
print(uid)
print(string)
print(weibo_url)
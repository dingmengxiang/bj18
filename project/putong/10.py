import requests
import re
response = requests.get('http://menxpat.com/list/post/29/1/1540884250')

# response.encoding = 'utf-8'
# print(response.content.decode())
#print(text)
text = response.content.decode()
print(text)
href_list = re.findall(r'<a href=\\"(http:\\/\\/menxpat.com\\/post.*?)"',text)
for href in href_list:
    print(href)
    href1 = re.sub(r'\\','',href)
    print(href1)
#href1 = re.sub('\\','',href)

# href1 = re.sub('\\','',href)
#
# print(href1)
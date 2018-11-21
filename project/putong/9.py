import re
a='十二月 30, 2018'
b=re.findall('(.{1,2})月',a)

duiying = {'十二':'12','十一':'11','十':10,'九':'09','八':'08','七':'07','六':'06','五':'05','四':'04','三':'03','二':'02','一':'01'}
keys = list(duiying.keys())
for key in keys:

    if key == b[0]:
       mouth = duiying[key]

       new = re.sub('.{1,2}月',mouth,a)
       print(new)
       time = ''.join(re.findall('(\d+) (\d+), (\d+)',new)[0])

       time = time[4:8] + time[0:4]
       print(time)
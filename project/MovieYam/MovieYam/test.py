import re
a='Nov.14 2018'
b = re.findall('(.*?\.)', a)

duiying = {'Dec.': '12', 'Nov.': '11', 'Oct.': '10', 'Sep.': '09', 'Aug.': '08', 'Jul.': '07', 'Jun.': '06', 'May.': '05', 'Apr.': '04', 'Mar.': '03', 'Fab.': '02', 'Jan.': '01'}
keys = list(duiying.keys())
for key in keys:

    if key == b[0]:
       mouth = duiying[key]
       new = re.sub('.*?\.', str(mouth), a)
       print(new)
       time = re.findall('(\d+) (\d+)', new)
       time = time[0][1]+time[0][0]

import  requests
headers={
    'Cookie':'_T_WM=414d2aac6c20dbbe3b8d1a0df2462c7c; SCF=AlnqwEWZmGC2U23oEp04JejHG5gEn_QP_0hJDf5aggjHg_LLU7QqKYOxNeflnxqGUcJi4HQN8AHdnJnh92oEjBY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGwFKTw7cNWVmgbZEEX_0s5JpX5K-hUgL.FoqNeKn7eoeEe0q2dJLoIE5LxK.L1KnLB.qLxKqL1KqLB-qLxK.LBK2LB.9.Mcx0qBtt; MLOGIN=1; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; SUB=_2A252zfoIDeRhGeBP6lcX9CzLwzuIHXVSMYZArDV6PUJbkdAKLVjXkW1NRZQT4z4oyeZUojhlxUbB_XTu6SjsIFNu; SUHB=0gHizexxnXOuK9; SSOLoginState=1539934808; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076032062377061','Host':'weibo.cn'
}
r=requests.get('https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%97%A0%E5%8F%8C+%E7%94%B5%E5%BD%B1',headers=headers)
print(r.text)
print(r.status_code)
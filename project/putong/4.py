import itchat
itchat.auto_login()#会有二维码出来，扫二维码
users=itchat.search_friends(name=u'Ronny')#可以是备注名字，也可以是昵称
userName=users[0]['UserName']
itchat.send(u'说出来你可能不相信，我在用命令给你发微信',userName)

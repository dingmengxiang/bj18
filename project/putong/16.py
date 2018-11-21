from tkinter import *
import random
import time

def ReStart():
    start = time.clock()
    global GameNumber
    GameNumber = random.randrange(1, 100)

ReStart()

root = Tk()
root.title("GuessNumber")

num = StringVar()
E1 = Entry(root,width = 5,textvariable = num,font=("", 40))
b = num.set('')

var = StringVar()
label = Label( root, textvariable=var,bg = 'red',width = 50,font=("", 20))
var.set("从1-100中随机选择一个数字，请你猜测这个数字是多少？")

def EnterClick(event):
    a = E1.get()
    isNum = a.isdigit()
    print(isNum)
    if isNum:
        number = int(a)
        if number > GameNumber:
            var.set("请输入小一点的数字" )
            b = num.set('')
        elif number < GameNumber:
            var.set("请输入大一点的数字" )
            b = num.set('')
        else:
            var.set("恭喜你，猜对了!是否继续游戏？(Y/N)")
            b = num.set('')
            end = time.clock()
    else:
        if a == 'y' or a == 'Y':
            ReStart()
            b = num.set('')
            var.set("从1-100中随机选择一个数字，请你猜测这个数字是多少？")
        elif a== 'n' or a =='N':
            root.destroy()
            b = num.set('')
        else:
            b = num.set('')

def onclick():
    a = E1.get()
    isNum = a.isdigit()
    print(isNum)
    if isNum:
        number = int(a)
        if number > GameNumber:
            var.set("请输入小一点的数字")
            b = num.set('')
        elif number < GameNumber:
            var.set("请输入大一点的数字")
            b = num.set('')
        else:
            var.set("恭喜你，猜对了!是否继续游戏？(Y/N)")
            b = num.set('')
    else:
        if a == 'y' or a == 'Y':
            ReStart()
            b = num.set('')
            var.set("从1-100中随机选择一个数字，请你猜测这个数字是多少？")
        elif a== 'n' or a =='N':
            root.destroy()
            b = num.set('')
        else:
            b = num.set('')

button = Button(root,text = "输入",font=("", 25),command =lambda:onclick())

E1.bind('<Return>',EnterClick)
button.pack(side = BOTTOM)

E1.pack(side = BOTTOM)
label.pack()
root.mainloop()

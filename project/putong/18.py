from tkinter import *
root = Tk()                     # 创建窗口对象的背景色
root.title("Australia daigou")  #窗口标题
# 窗口大小
width, height = 450, 450
# 窗口居中显示
root.geometry('%dx%d+%d+%d' % (width, height,(root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2))
# 窗口最大值
root.maxsize(600, 600)
# 窗口最小值
root.minsize(400, 400)

# 顶部标签
label = Label(root, text="Please enter the URL address")
label.pack()

# 全局变量，用于接收对话框输入的值。
global input_text
input_text = StringVar()
# 中部输入框
entry = Entry(root, textvariable=input_text, width=100)
input_text.set('http://www.baidu.com')
entry.pack()

#单选框
global radio_value
radio_value = StringVar()
radio_value.set('csv')
Radiobutton(root,variable = radio_value, text='csv(no image)', value = 'csv').pack()
Radiobutton(root,variable = radio_value, text='xlsx(incloud image. very slow)', value ='xlsx' ).pack()
def dell():
    print("开始爬虫啦")
    for i in range(5):
        text.insert(END, '正在下载第' + str(i) + '页...\n')
        #text.update()
# body部按钮
button = Button(root, text="Download file", command=dell)  #创建按钮

button.pack()

# 底部返回信息
global text
text = Text(root)
s = Scrollbar(root)
s.pack(side=RIGHT, fill=Y)
text.pack(side=LEFT, fill=Y)
s.config(command=text.yview)
text.config(yscrollcommand=s.set)

root.mainloop()

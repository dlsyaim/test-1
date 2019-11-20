# 导入tkinter和随机模块
from tkinter import *
import random


# 定义复制到剪切板函数
def clip(list):
    root.clipboard_clear()
    root.clipboard_append(list)

    
# 定义随机双色球函数
def rand1():
    numlist1=random.sample(range(1,34),6)
    numlist1.sort()
    numlist1.append(random.sample(range(1,17),1))
    e1.delete(0,END)
    e1.insert(0,numlist1)
    clip(numlist1)


# 定义随机大乐透函数
def rand2():
    numlist2=random.sample(range(1,36),5)
    numlist2.sort()
    numlist3=random.sample(range(1,13),2)
    numlist3.sort()
    numlist2=numlist2 + numlist3
    e2.delete(0,END)
    e2.insert(0,numlist2)
    clip(numlist2)


# 主窗体
root = Tk()
root.title('彩票号码生成器')


# 标签1和2
Label(root, text='双色球随机号：').grid(row=0)
Label(root, text='大乐透随机号：').grid(row=1)


# 输出框1和2
e1=Entry(root)
e2=Entry(root)
e1.grid(row=0, column=1, padx=10, pady=5)
e2.grid(row=1, column=1, padx=10, pady=5)


# 按钮1和2
theButton1 = Button(root, text="生成", command=rand1)
theButton1.grid(row=0,column=2,padx=10,pady=5)
theButton2 = Button(root, text="生成", command=rand2)
theButton2.grid(row=1,column=2,padx=10,pady=5)


# 主窗体循环
mainloop()

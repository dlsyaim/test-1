#0.初始化，导入模块
import os
import time
import shutil



#1.定义列表
la=[]    #用来存所有文件和文件节名
lb=[]    #用来存所有文件名
lc=[]    #存所有文件的时间戳
ld=[]    #存去重复的列表lc



#2.获取需要归档的log文件夹下所有文件和文件夹名，放入到列表la中
os.chdir("C:\\e\\SUZHOU\\Log")    #首先跳转工作目录到这个log目录
la=os.listdir(os.getcwd())    #把当前目录的文件名和文件夹名称存储列表la



#3.判断列表la的元素是否是文件，是文件，导入列表lb
for i in la:
    if os.path.isfile(i):    #判断是否是文件
        lb.append(i)



#4.获取列表lb中的文件的时间戳，生成列表lc
for i in lb:
    t=time.strftime("%Y%m%d",time.localtime(os.path.getmtime(i)))    #文件时间格式调整为YYYYMMDD样式
    lc.append(t)



#5.去除列表lc的重复项，生成列表ld
ld=list(set(lc))    #set方法去除重复后生成



#6.遍历ld，判断是否存在相应名称的文件夹，不存在就创建，存在就跳过
for i in ld:
    if os.path.isdir(i+"-log") == False:
        os.mkdir(i+"-log")



#7.移动文件到对应时间的文件夹
for i in range(len(lb)):
    shutil.move(lb[i],lc[i]+"-log")

#!/usr/bin/python
# -*- coding: UTF-8 -*-

# os用以使用系统命令，time打印时间或延时，requests发送http post。
import os
import time
import requests


# 准备http头部和数据，原自网页查看
headers={
"Host": "192.0.2.100",
"User-Agent": "Mozilla/5.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding": "gzip, deflate, br",
"Content-Type": "application/x-www-form-urlencoded",
"Content-Length": "156",
"Origin": "https://192.0.2.100",
"Connection": "keep-alive",
"Referer": "https://192.0.2.100/login.html?redirect=192.0.2.100/",
"Upgrade-Insecure-Requests": "1"
}

data={
"buttonClicked":"4",
"err_flag":"0",
"err_msg":"",
"info_flag":"0",
"info_msg":"",
"redirect_url":"http%3A%2F%2F192.0.2.100%2F",
"network_name":"Guest+Network",
"username":"VIP12",
"password":"123456"
}


# 定义循环子函数
def autowifi():
    while (True):
        # ping 外网3次，每次等5秒
        result = os.system(u"ping 1.2.4.8 -c 3 -W 5")
        if result != 0:
            # 如果ping失败，主动重连，并重新获取ip
            try:
                os.system(u"iw wlan0 disconnect")
                # sleep让程序暂停，主要让前一个命令有充分的时间执行完
                time.sleep(5)
                os.system(u"iw wlan0 connect jabil_visitors")
                time.sleep(5)
                os.system(u"dhclient wlan0")
                time.sleep(10)
                # 模拟认证
                r=requests.post('https://192.0.2.100/login.html',data=data,headers=headers,verify=False)
                time.sleep(5)
                # 打印当前时间和post的结果
                print(time.asctime(time.localtime(time.time())),r.status_code)
            except Exception as e:
                # 如果有报错，打印出来，但不结束程序
                print(e)
        else:
            # 如果ping成功，打印时间+normal
            print(time.asctime(time.localtime(time.time())),"normal")
        print("="*50)
        # 程序休息10分钟
        time.sleep(600)

# 主语句调用函数
if __name__=='__main__':
    autowifi()

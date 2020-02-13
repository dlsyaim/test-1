#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import requests
import commands


# define hadears and data.
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


# cycle func.
def cyc():
    while (True):
        while ping() == 0:
            ipck()
            auth()
        print(time.asctime(time.localtime(time.time())),"normal")
        print("="*50)
        time.sleep(900)


# ip check
def ipck():
    try:
        while commands.getoutput('iw wlan0 link| wc -l') != 1:
            os.system(u"iw wlan0 disconnect")
            time.sleep(5)
        while commands.getoutput('iw wlan0 link| wc -l') == 1:
            os.system(u"ifdown wlan0")
            time.sleep(10)
            os.system(u"ifup wlan0")
            time.sleep(10)
            os.system(u"iw wlan0 connect jabil_visitors")
            time.sleep(50)
        while commands.getoutput('ifconfig wlan0|grep "inet addr"| wc -l') ==0:
            os.system(u"killall dhclient")
            time.sleep(3)
            os.system(u"dhclient wlan0")
            time.sleep(10)
            os.system(u"ip route add default via 10.136.14.1 dev wlan0")
            time.sleep(10)
    except Exception as e:
        print(e)


# set nic and auth
def auth():
    try:
        r = requests.post('https://192.0.2.100/login.html', data=data, headers=headers, verify=False)
        time.sleep(5)
        print(time.asctime(time.localtime(time.time())),r.status_code)
    except Exception as e:
        print(e)


# ping
def ping():
    count = 0
    for n in range(5):
        result = os.system(u"ping 1.2.4.8 -c 1 -W 5")
        if result == 0:
            count += 1
    return count


# call
if __name__=='__main__':
    cyc()

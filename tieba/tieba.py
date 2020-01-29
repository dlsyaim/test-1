#!/usr/bin/env python
# -*- coding: utf-8 -*-

# requests模拟发起http，time用于打印时间
import requests
import time
 
 
 
# url固定的
url = 'https://tieba.baidu.com/tbmall/onekeySignin1'
 
 
# 把请求头制作成字典
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "tieba.baidu.com",
    "Refer": "https://tieba.baidu.com/index.html",
    "Cookie": "TIEBA_USERTYPE=18658700de1e8f842ed81648; BAIDUID=FC561B40E910ADEF94887D62CF306E65:FG=1; TIEBAUID=240918a99f647b3abf3f8383; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1580004689,1580029385,1580030020,1580030118; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1580030314; BDUSS=X5KT1o0eUFXQVJ0RGFPT35QNG82Vi1SVVVXVUljZUJOd0k1bzJKdlhEcFQ1bFJlSUFBQUFBJCQAAAAAAAAAAAEAAAAQTRwgQ3JpdGljMjAxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFNZLV5TWS1eM; STOKEN=0098802104ccad1432d0fbe4d06d1d9a8634dad014f8f4609ce1c8c445863599",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "X-Requested-With": "XMLHttpRequest"
}
 
# 把表单数据制作成字典
data={"ie": "utf-8", "tbs": "95b8e93ebde16bbf1580030293"}
 
# 发起自动签到
r = requests.post(url,headers=headers,data=data)
 
# 查看结果
print(time.asctime(time.localtime(time.time())),r.status_code)

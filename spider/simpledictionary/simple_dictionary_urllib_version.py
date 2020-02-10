from urllib import request, parse
from urllib.parse import quote
from lxml import etree
from tkinter import *
import json


# 英文单词查询网址
ebase = 'http://dict.youdao.com/w/eng/'
# 中文单词查询网址
cbase = 'http://dict.youdao.com/w/'
# 翻译网址
trans = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
# 查询时http头
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}
# 翻译提交的字典
dic = {"doctype": "json"}


# 判断查询类型
def chaxun():
    if v.get() == 1:
        chaci()
    else:
        fanyi()


# 查词 chaci():
def chaci():
    wd = e1.get()
    if '\u4e00' <= wd <= '\u9fff':
        # 如果是中文查询，转换中文为URL编码格式
        wd = quote(wd)
        url = cbase + wd
        q = request.Request(url=url, headers=headers)
        r = request.urlopen(q, timeout=2)
        html = etree.HTML(r.read().decode('utf-8'))
        result = html.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/p/span/a/text()')
    else:
        url = ebase + wd
        q = request.Request(url=url, headers=headers)
        r = request.urlopen(q, timeout=2)
        html = etree.HTML(r.read().decode('utf-8'))
        result = html.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/text()')
    # 清理text，重新显示
    text1.delete(1.0, END)
    # 如果有结果，显示结果
    if len(result) != 0:
        for pt in result:
            text1.insert(INSERT, pt + '\n')
    else:
        # 如果没有结果，提示没有结果
        text1.insert(INSERT, 'There is no explain.')


# 翻译
def fanyi():
    text1.delete(1.0, END)
    wd = e1.get()
    dic['i'] = wd
    data = bytes(parse.urlencode(dic), encoding='utf-8')
    q = request.Request(url=trans, data=data, headers=headers, method='POST')
    r = request.urlopen(q)
    result = json.loads(r.read().decode('utf-8'))
    text1.insert(INSERT, result['translateResult'][0][0]['tgt'])


if __name__ == '__main__':
    # 主函数，定义一个tk对象
    root = Tk()
    root.title('简易有道字典')
    l1 = Label(root, text='请输入要查询的内容：')
    l1.grid(row=0)
    e1 = Entry(root)
    e1.grid(row=0, column=1, padx=10, pady=5)
    bt1 = Button(root, text='查询', command=chaxun)
    bt1.grid(row=0, column=2, padx=10, pady=5)
    text1 = Text(root, width=59, height=10)
    text1.grid(row=1, columnspan=5, pady=7)
    v = IntVar()
    v.set(1)
    Radiobutton(root, text="查词", variable=v, value=1).grid(row=0, column=3)
    Radiobutton(root, text="翻译", variable=v, value=2).grid(row=0, column=4)
    mainloop()

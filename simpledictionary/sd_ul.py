from urllib import request
from urllib.parse import quote
from lxml import etree
from tkinter import *


# 英文查询
ebase = 'http://dict.youdao.com/w/eng/'
# 中文查询
cbase = 'http://dict.youdao.com/w/'
# 查询时http头
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}


# 查询函数
def chaxun():
    wd = e1.get()
    if '\u4e00' <= wd <= '\u9fff':
        # 如果是中文查询，转换中文为URL编码格式
        wd = quote(wd)
        url = cbase + wd
        q = request.Request(url=url, headers=headers)
        r = request.urlopen(q)
        html = etree.HTML(r.read().decode('utf-8'))
        # 获取查询结果
        result = html.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/p/span/a/text()')
    else:
        url = ebase + wd
        q = request.Request(url=url, headers=headers)
        r = request.urlopen(q)
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


if __name__ == '__main__':
    # 主函数，定义一个tk对象
    root = Tk()
    root.title('简易有道字典')
    l1 = Label(root, text='请输入要查询的单词：')
    l1.grid(row=0)
    e1 = Entry(root)
    e1.grid(row=0, column=1, padx=10, pady=5)
    bt1 = Button(root, text='查询', command=chaxun)
    bt1.grid(row=0, column=2, padx=10, pady=5)
    text1 = Text(root, width=45, height=10)
    text1.grid(row=1, columnspan=3)
    mainloop()

# _*_ coding: utf-8 _*_
# Developer: suchocolate
# Date: 4/1/2020 21:07
# File name: meinv.py
# Development tool: PyCharm



import requests
from lxml import etree
import os


# 主函数
def main(num):
    # 检查目录
    ckdir()
    # 图片计数
    n = 1
    # 逐页下载
    for x in range(num):
        # 第一页的url和其他页不同
        if x == 0:
            url = url1
        else:
            url = url2 + str(x * 50)
        imgs = get_url(url)
        print('开始下载第' + str(x + 1) + '页')
        n = dl_img(imgs, n)
    print('下载完成，共下载' + str(n) + '张')


# 创建存储图片的目录，可根据细化更改名称
def ckdir():
    if os.path.isdir('meinv') == False:
        os.mkdir("meinv")


# 分析页面图片的url
def get_url(url):
    # 登陆论坛页面
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    # 过滤出贴子url
    result1 = html.xpath('//div[contains(@class, "threadlist_title")]/a/@href')
    img_urls = []
    # 进入各个贴子
    for sfx in result1:
        r = requests.get(base_url + sfx, headers=headers)
        print('获取页面' + sfx + '的图片地址...')
        html = etree.HTML(r.text)
        # 查找贴子内的图片链接
        result2 = html.xpath('//img[@class="BDE_Image"]/@src')
        # 如果图片链接不为空的话，放入到图片链接列表
        if len(result2) != 0:
            for x in result2:
                img_urls.append(x)
    return img_urls


# 下载图片
def dl_img(img_urls, n):
    num = str(len(img_urls))
    print('有' + num + '张照片要下载。')
    # 遍历图片链接列表
    for img in img_urls:
        r = requests.get(img, headers=headers)
        pic_name = img.split('/')[-1]
        with open('meinv\\' + pic_name, 'wb') as f:
            f.write(r.content)
        print('已下载' + pic_name + '，共下载' + str(n) + '张。')
        n = n + 1
    return n


if __name__ == '__main__':
    # 设置基础参数
    headers = {'user-agent': 'firefox'}
    # url1是美女吧的网址，可根据需要自行更换，复制浏览器地址，粘贴到这里即可
    url1 = 'https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&fr=index&fp=0&ie=utf-8'
    # url2是美女吧非第一页的网址，后面的字稍有变化，大家自行更换
    url2 = 'https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn='
    base_url = 'https://tieba.baidu.com'
    page_num = input('请输入下载的几页的贴子：')
    page_num = int(page_num)
    main(page_num)


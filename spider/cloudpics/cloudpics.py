import requests
from lxml import etree
import imageio
import re
import pyglet
import os


# 存储当天12张图
def ckdir():
    if os.path.exists('wxyt_pic') == False:
        os.mkdir('wxyt_pic')


# 获取图片url列表
def getpage(page):
    try:
        r = requests.get(page, headers=headers)
        html = etree.HTML(r.text)
        result = html.xpath('//script[@type="text/javascript"]/text()')[2]
        urls = re.findall('/product.*.JPG', result)
        return urls
    except Exception as e:
        print(e)


# 下载图片
def dlpic(urls):
    filenames = []
    for item in urls:
        r = requests.get(base_url + item, headers)
        filename = item.split('/')[-1]
        filenames.append(filename)
        with open('wxyt_pic\\' + filename, 'wb') as f:
            f.write(r.content)
        print('已下载：'+item)
    return filenames


# 制作gif
def makegif(images):
    frames = []
    images.reverse()
    for item in images:
        frames.append(imageio.imread('wxyt_pic\\'+item))
    imageio.mimsave('hecheng.gif', frames, 'GIF', duration=1)


# 播放gif
def playgif(seq=0):
    if set == 0:
        #播放12张合成好的gif
        animation = pyglet.resource.animation('hecheng.gif')
    else:
        pyglet.resource.path = ['wxyt_pic']
        la = os.listdir('wxyt_pic')
        images = []
        for n in la:
            images.append(pyglet.resource.image(n))
        #播放库存中的所有照片
        animation = pyglet.image.Animation.from_image_sequence(images, period=0.5, loop=True)
    #显示动画
    sprite = pyglet.sprite.Sprite(animation)
    windows = pyglet.window.Window(width=sprite.width, height=sprite.height)
    @windows.event
    def on_draw():
        windows.clear()
        sprite.draw()
    pyglet.app.run()


# init
if __name__ == '__main__':
    base_url = 'http://image.nmc.cn'
    page = 'http://www.nmc.cn/publish/satellite/fy2.htm'
    headers = {"user-agent": "firefox"}
    ckdir()
    urls = getpage(page)
    images = dlpic(urls)
    makegif(images)
    # 0只播放今天12张，1播放库存里所有照片
    playgif(1)



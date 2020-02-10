import requests
from lxml import etree
import imageio


# init
base_url = 'http://image.nmc.cn'
page = 'http://www.nmc.cn/publish/satellite/fy2.htm'
headers = {"user-agent": "firefox"}


def getpage():
    try:
        r = requests.get(page, headers=headers)
        if r.status_code == 200:
            html = etree.HTML(r.text)
            result = html.xpath('//script[@type="text/javascript"]/text()')[2]
            urls = re.findall('/product.*.JPG',result)
            return urls
    except Exception as e:
        print(e)


def downtu(urls):
    filenames = []
    for item in urls:
        r = requests.get(base_url + item, headers)
        filename = item.split('/')[-1]
        filenames.append(filename)
        with open('wx\\' + filename,'wb') as f:
            f.write(r.content)
        print('已下载：'+item)
    return filenames


def makegif(images):
    frames = []
    images.reverse()
    for item in images:
        frames.append(imageio.imread('wx\\'+item))
    imageio.mimsave('hecheng.gif', frames, 'GIF', duration=1)


# init
if __name__ == '__main__':
    urls = getpage()
    images = downtu(urls)
    makegif(images)
    print('图像下载完成。')


import requests
from lxml import etree
from urllib.parse import urlencode
import re
import random

# 初始化常量
base_url = 'https://www.weibo.com/p/aj/album/loading?'
img_base_url = 'https://wx3.sinaimg.cn/large/'
headersd = {'user-agent': 'firefox'}
headers = {
    "Host": "www.weibo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Cookie": "SUB=_2A25zRGbhDeRhGedO6VAS8CvJyTyIHXVQMN8prDV8PUNbmtAfLUSskW9NInBbEhmNi1Chc3qP2y_a79R1PnFhCQrN; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5J7ijbK0W-si0H1uRNNg4z5JpX5K2hUgL.Fo27eoz0eh-feo52dJLoIpjLxK"
              "-L1K5LBoBLxK-LBKBLBKMLxK-L12BLB-zt; SINAGLOBAL=2662989062002.8574.1581256923804; "
              "ULV=1581258332493:2:2:2:8214765949922.557.1581258332491:1581256923835; "
              "login_sid_t=579cc2c57f5be3af70293e47f8178839; cross_origin_proto=SSL; "
              "Ugrow-G0=d52660735d1ea4ed313e0beb68c05fc5; YF-V5-G0=7a7738669dbd9095bf06898e71d6256d; "
              "WBStorage=42212210b087ca50|undefined; _s_tentry=-; wb_view_log=1536*8641.25; "
              "Apache=8214765949922.557.1581258332491; "
              "SCF=Al5MHPfWLljcZYNaknea9Zejv_lngVOC6O9HcVAuLt2GrYRGm_04sMziQRSt1gIORQSL_1ezBGi8Pc2r2ViqJg0.; "
              "SUHB=0xnELvDbxuhmMi; ALF=1612794414; SSOLoginState=1581258416; un=wijkr3; wvr=6; "
              "YF-Page-G0=ae24d9a5389d566d388790f1c25a266b|1581258506|1581258420; "
              "wb_view_log_1022305520=1536*8641.25; "
              "webim_unReadCount=%7B%22time%22%3A1581258444965%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0"
              "%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D "
}


def set_para(oid, pid, since, offset):
    ri = "".join(random.choices('0123456789', k=13))
    params = {
        "ajwvr": "6",
        "type": "photo",
        "owner_uid": oid,
        "viewer_uid": "1022305520",
        "page_id": pid,
        "since_id": since,
        "page": offset,
        "ajax_call": "1",
        "__rnd": ri
    }
    return params


def get_url(oid, pid, offset):
    result = []
    since = 1
    for n in range(1, offset + 1):
        params = set_para(oid, pid, since, n)
        page_url = base_url + urlencode(params)
        # 请求一页
        r = requests.get(page_url, headers=headers)
        r = r.json().get('data')
        html = etree.HTML(r)
        # 收集图片url
        page = html.xpath('//img[@class="photo_pict"]/@src')
        for item in page:
            result.append(re.split('[/?]', item)[4])
        # 分析下一页请求的参数since
        st = html.xpath('//div[contains(@class, "WB_cardwrap")]/@action-data')
        if len(st) == 0:
            print('共'+str(len(result))+'张图片。')
            return result
        since = st[0].split('=')[4]
    print('共' + str(len(result)) + '张图片。')
    return result


def dl_image(img_list):
    n = 1
    for item in img_list:
        r = requests.get(img_base_url + item, headers=headersd)
        with open("ns\\" + item, 'wb') as f:
            f.write(r.content)
        print('已下载：' + item + '，共下载' + str(n) + '张。')
        n = n + 1


if __name__ == '__main__':
    url = input('请输入相册网址： ')
    num = input('请输入想下载的页数：')
    #url = 'https://weibo.com/p/1005055528213114/photos?from=page_100505&mod=TAB'
    owner_id = url.split('/')[4][6:]
    page_id = url.split('/')[4]
    #num = 10
    img_urls = get_url(owner_id, page_id, num)
    dl_image(img_urls)


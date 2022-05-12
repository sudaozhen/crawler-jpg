'''
File         : 
version      : 
Author       : Su Daozhen
Date         : 2022-04-23 18:08:06
LastEditors  : Su Daozhen
LastEditTime : 2022-04-23 21:09:04
Encoding     : UTF-8
Description  : 
Attention    : 
********************COPYRIGHT 2021 Su Daozhen********************
'''
import os
import shutil
# from urllib import response
import requests
from bs4 import BeautifulSoup
import re

headers = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
"Accept-Encoding": "gzip, deflate, sdch", 
"Accept-Language": "zh-CN,zh;q=0.8", 
"Cennection": "close",
"Cookie": "_gauges_unique_hour=1; _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1",
"Referer": "http://www.cnu.cc/",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

url = 'http://www.cnu.cc/works/575043'

# 下载函数
def download_jpg(image_url, image_localpath):
    response = requests.get(image_url, stream=True)
    # 正常返回200，异常返回404
    if response.status_code == 200:
        with open(image_localpath, 'wb') as f:
            response.raw.deconde_content = True
            shutil.copyfileobj(response.raw, f)

def craw3(url):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')

    # print(soup.prettify())

    for pic_href in soup.find_all('div', class_='article-container'):
        # print(pic_href.prettify())

        for pic1_href in pic_href.find_all('div', id='imgs_json'):
            # print(pic1_href.prettify())
            pattern = re.compile(r',*?img"."(.*?)"."', re.S)
            results = re.findall(pattern, pic1_href.text)
            
            for i in range(0,len(results)-1,1):
                # print(results[i])
                imgurl = 'http://imgoss.cnu.cc/' + results[i]
                dir = os.path.abspath('./img')
                filename = os.path.basename(imgurl)  # url仅保留文件名称
                imgpath = os.path.join(dir, filename)
                print('开始下载 %s' % imgurl)
                download_jpg(imgurl, imgpath)
craw3(url)

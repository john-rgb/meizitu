# coding:utf8
'''
爬取所有xx标签下的所有妹子的图片并保存到妹子图的目录下
'''
import json
import os
import re

import requests
from urllib.parse import urlencode
import urllib.request
from json.decoder import JSONDecodeError
import threading

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def get_page_index(url):#获取网页上的所有内容
    try:
        reponse = requests.get(url)
        # print(reponse.text)
        if reponse.status_code == 200:
            soup=BeautifulSoup(reponse.content,'lxml')
            return soup
        return None
    except RequestException:
        print('请求页面出错！')
        return None
def has_a_and_target(tag):#获取有target的 href内容
    return tag.has_attr('href') and tag.has_attr('target')
def parse_page(rep):
    content=rep.find_all('li',class_="wp-item")
    contents=[]
    for i in content:
        contents.append(i.a.attrs['href'])
    return contents
def parse_pic_page(html):#获取图片连接
    ti1=[]
    ti=html.head.title.string
    for s in ti.split(" | "):
        ti1.append(s)
    pic=html.find_all('div',id='picture')
    picurl=[]
    for i in pic:
        img=i.find_all('img')
        for j in img:
            picurl.append(j.attrs['src'])
    return picurl,ti1[0]
def download_image(url,dirname,filename):#下载图片
    if os.path.exists(dirname):
        save_image(url,filename)
        # print(url)
        # save_image(url,filename)
    else:
        os.mkdir(dirname)
        # print(url)
        save_image(url, filename)
def save_image(url,filename):#保存图片
    print(url)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    reponse=requests.get(url,headers=headers)
    file=open(filename,'wb')
    file.write(reponse.content)
    file.close()
    # print(reponse.content)
def get_page_list(url):#获取图片页面数
    pagelist=[]
    pagelist.append(url)
    html=get_page_index(url)
    pagenum=get_last_num(html.find_all('ul'))
    if  pagenum:
        for i in range(2,int(pagenum)+1):
            replace='sexy_'+str(i)
            pagelist.append(url.replace('sexy',replace))
        return pagelist
    else:
        return None
def get_last_num(content):#获取页面数字
    p='<li><a href="sexy_([0-9]{2}).html">末页</a></li>'
    pattern=re.compile(p,re.S)
    result=re.search(pattern,str(content))
    if result:
        return result.group(1)
    else:
        return None
def main():
    url='http://www.meizitu.com/a/sexy.html'
    pagelist=get_page_list(url)
    for urlnum in pagelist:
        reponse=get_page_index(urlnum)
        list=parse_page(reponse)
        for i in list:
            num=0
            pic_html=get_page_index(i)
            picurl,title=parse_pic_page(pic_html)
            for pu in picurl:
                filename = './' + title + '/' + title + str(num) + '.jpg'
                num+=1
                print('正在保存'+filename)
                # print(pu)
                th=threading.Thread(target=download_image,args=(pu,title,filename))
                th.start()


    # print(reponse)
if __name__=='__main__':
    main()
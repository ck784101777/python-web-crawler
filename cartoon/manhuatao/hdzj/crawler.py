#!/usr/bin/env python3

import urllib.request
import re
import os

#函数：下载网址
#参数：url:用于保存网址地址 fname:网址文件名
def get_web(url,fname):
  #头信息，用于反爬虫
  header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
  request=urllib.request.Request(url,headers=header)
  #将网址内容存入html
  html=urllib.request.urlopen(request)
  #创建文件
  with open(fname,mode='wb') as f:
    f.write(html.read())
  html.close()

#函数：正则匹配漫画中的图片url
#参数: fname:下载到本地的网址文件,*.html dirname:下载图片后存放的目录
def get_photo(fname,dirname):
  #加载图片的正则表达式
  cpatt=re.compile("images\\\\\/comic\\\\\/\d+\\\\\/\d+\\\\\/\w+\.jpg")
  #打开文件
  with open(fname) as f:
    data=f.read()
    #匹配图片url,返回一个列表
    m=cpatt.findall(data)
    if m:
       #图片的序号,从1开始，可自定义
       num=1
       #遍历列表中的图片url
       for i in m:
         #将url分片，分成一个列表
         mylist=re.split("\\\\/",i)
         #组成可供下载url
         url="https://res.nbhbzl.com//images/comic/%s/%s/%s"%(mylist[2],mylist[3],mylist[4])
         #如果目录不存在，创建
         pdir="/python/bhzjp/%s"%(dirname)
         if not os.path.exists(pdir): 
           os.mkdir(pdir)
         #拼接目录文件名
         fname="%s%d.jpg"%(pdir,num)
         num+=1
         #下载图片
         get_web(url,fname)


if __name__=='__main__':
#  for i in range(145498,145615):
#      get_web("https://www.manhuatao.com/manhua/4750/%d.html"%(i),"/python/bhzj/%d.html"%(i))
#dir是我存放网页文件的路径
#我是先将网页文件下载后再下载的图片，具体的操作要根据漫画图片的url调整 
  dirs=os.listdir('/python/bhzj')
  for i in dirs:
    dirname=re.match("\d+",i)
    get_photo("/python/bhzj/%s"%(i),dirname.group())
    
 

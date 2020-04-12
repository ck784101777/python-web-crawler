# -*- coding: utf-8 -*-
import scrapy
import json
import re
from urllib import parse
from ..items import BaiduimageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.baidu.com']
    word_origin = input("请输入搜索关键字：")
    word = parse.quote(word_origin)
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&is=&fp=result&queryWord=" + word + "&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=" + word + "&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30&gsm=1e&1586660816262="

    def start_requests(self):
        for pn in range(30,151,30):
            url=self.url.format(pn)
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        regex = '"thumbURL":"(.*?)"'
        pattern = re.compile(regex, re.S)
        links = pattern.findall(response.text)
        item=BaiduimageItem()
        item["word"]=self.word_origin
        for i in links:
            item["link"]=i

            yield item

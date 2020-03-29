# -*- coding: utf-8 -*-
import scrapy
from ..items import Novelcrapy2Item

class QuanbenSpider(scrapy.Spider):
    name = 'quanben'
    allowed_domains = ['www.qb5.tw']
    start_urls = ['http://www.qb5.tw']

    # 一级解析：获取主题
    def parse(self, response):
        topic_list = response.xpath('//div[@class="head_t"]/ul/li[position()>1 and position()<9]')
        for i in topic_list:
            novel_topic = i.xpath('./a/@title').get()
            link = i.xpath('./a/@href').get()

            yield scrapy.Request(
                url=link,
                meta={'novel_topic':novel_topic},
                callback=self.parse_page
            )


    # 二级解析：遍历页码数
    def parse_page(self,response):
        novel_topic = response.meta['novel_topic']
        #<a href="https://www.qb5.tw/list/1/373.html" class="last">373</a>
        page_count = response.xpath('//div[@class="pagelink"]/a[@class="last"]/text()').get()
        url=response.url
        page_count=1
        for i in (1,page_count+1,1):
            link=url[:-5] + "/" + str(i) + ".html"
            yield scrapy.Request(
                url=link,
                meta={'novel_topic':novel_topic},
                callback=self.parse_two
            )

    # 二级解析：获取主题下小说
    def parse_two(self, response):
        novel_topic = response.meta['novel_topic']
        novle_lists = response.xpath('//div[@class="zp"]')
        for i in novle_lists:
            novel_name = i.xpath('./a/@title').get()
            link = i.xpath('./a/@href').get()
            yield scrapy.Request(
                url=link,
                meta={'novel_topic':novel_topic,'novel_name':novel_name},
                callback=self.parse_three
            )

    # 三级解析：获取小说章节
    def parse_three(self,response):
        novel_topic = response.meta['novel_topic']
        novel_name = response.meta['novel_name']
        chapter_list=response.xpath('//dd')
        for i in chapter_list:
            novel_chapter=i.xpath('./a/text()').get()
            # 不同网站的章节处理方式不一样，有些是绝对路径，有些是相对路径
            # 如果是相对路径就需要拼接
            link=self.start_urls[0]+i.xpath('./a/@href').get()
            yield scrapy.Request(
                url=link,
                meta={'novel_topic':novel_topic,'novel_name':novel_name,'novel_chapter':novel_chapter},
                callback=self.parse_fuor
            )

    # 四级解析：获取小说内容
    def parse_fuor(self,response):
        novel_topic = response.meta['novel_topic']
        novel_name = response.meta['novel_name']
        novel_chapter = response.meta['novel_chapter']

        item = Novelcrapy2Item()
        item['novel_topic']= novel_topic
        item['novel_chapter'] = novel_chapter
        item['novel_name'] = novel_name
        item['novel_content']=response.xpath('//div[@id="content"]/text()').extract()

        yield item

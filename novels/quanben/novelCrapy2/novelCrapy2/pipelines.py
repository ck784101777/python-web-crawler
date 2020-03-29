# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class Novelcrapy2Pipeline(object):


    def process_item(self, item, spider):
        # D:\\小说\\主题\\斗破苍穹\\第一章   这样的形式，加后缀就即可 这里做成.txt格式的文本
        dir = "D:\\小说\\" + item['novel_topic'] + "\\" + item['novel_name']
        if not os.path.exists(dir):
            os.makedirs(dir)

        #章节有可能有空格，存文件不允许有空格字符，所以要做下处理
        filename=dir + "\\" + item['novel_chapter'].replace('','_') + ".txt"
        with open(filename,'w',encoding="utf-8") as f:
             f.write("".join(item['novel_content']))

        print('ok')

        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes

class BaiduimagePipeline(ImagesPipeline):

    word=""

    def get_media_requests(self, item, info):
        self.word=item['word']
        yield scrapy.Request(url=item['link'])

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return self.word + '/%s.jpg' % (image_guid)

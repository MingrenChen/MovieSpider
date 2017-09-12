# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class DyttPipeline(object):
    def __init__(self):
        # self.f2 = open('euromovie.json', 'wb')
        self.f = open("a.txt","w")

    def process_item(self, item, spider):
        # print(item["pic"])
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.f.close()

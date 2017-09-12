# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql


class DyttPipeline(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "6966xx511", "testDB", charset='utf8mb4', )
        self.cursor = self.db.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS MOVIE")
        sql = """CREATE TABLE MOVIE (
                 name  VARCHAR(255) NOT NULL,
                 rate  VARCHAR(255),
                 time  int,
                 link  VARCHAR(255),
                 category VARCHAR(255),
                 url VARCHAR(255)
                 );"""
        self.cursor.execute(sql)
        self.db.commit()
        self.f = open("a.txt", "wb")

    def process_item(self, item, spider):
        self.cursor.execute("ALTER TABLE MOVIE CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;")
        if not self.cursor.execute("SELECT * FROM MOVIE WHERE name = '{}'".format(item['name'])):
            sql = """INSERT INTO MOVIE(name,rate,time,link,category,url)
                                      VALUES ('{}','{}','{}','{}','{}','{}');""".format\
                (item['name'],item['rate'], item['time'], item['link'],
                 str(item['category']),item['url'])
            self.cursor.execute(sql)
            self.db.commit()
            content = json.dumps(dict(item), ensure_ascii=False)
            self.f.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.f.close()

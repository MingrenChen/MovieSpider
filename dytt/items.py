# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DyttItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    rate = scrapy.Field()
    time = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    pic = scrapy.Field()

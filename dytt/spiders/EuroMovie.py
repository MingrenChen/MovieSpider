# -*- coding: utf-8 -*-
import urllib
import re,os,sys
import scrapy
import scrapy.selector
import urllib.parse
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import items

class EuromovieSpider(scrapy.Spider):
    name = 'EuroMovie'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/oumei/list_7_1.html']

    def parse(self, response):
        for movie_box in response.xpath("//table[@class=\"tbspan\"]"):
            url = urllib.parse.urljoin('http://www.ygdy8.net', movie_box.xpath("tr[2]/td[2]/b/a[2]/@href").extract()[0])
            yield scrapy.Request(url, callback=self.parse_movie)
        next_page = response.xpath("//div[@class=\"x\"]/td/a/@href").extract()[-2]
        if next_page:
            next_page_url = urllib.parse.urljoin('http://www.ygdy8.net/html/gndy/oumei/', next_page)
            print(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_movie(self, response):
        item = items.DyttItem()
        full_title = response.xpath("//*[@id=\"header\"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/h1/font/text()").extract()[0]
        item['name'] = re.search("《.*》", full_title).group(0)
        item['time'] = full_title[:4]
        content = response.xpath("//*[@id=\"Zoom\"]/td").extract()[0].split("<br>")
        item["category"] = content[8][6:].split("/")
        item['rate'] = content[12]
        item['link'] = response.xpath("//div[@id=\"Zoom\"]/td/table/tbody/tr/td/a/@href").extract()[0]
        yield item



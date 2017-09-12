# -*- coding: utf-8 -*-
import urllib
import re, os, sys
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
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_movie(self, response):
        item = items.DyttItem()
        content = response.xpath("//*[@id=\"Zoom\"]/td").extract()[0].split("<br>")
        item['url'] = response.url
        for k in content:
            if "译　　名" in k:
                item['name'] = k[6:].split("/")[0]
                break
        if item['name'] == None:
            for ak in content:
                if "片　　名" in ak:
                    item['name'] = ak[6:]
                    break
        for j in content:
            if "年　　代" in j:
                item['time'] = j[6:10]
                break
        for i in content:
            if "类" in i:
                item["category"] = i[6:]
                break
        try:
            item['rate'] = response.xpath("//*[@id=\"Zoom\"]/td").re("IMDb.+\d.\d\/10","i")[0][-6:]
        except:
            item['rate'] = None
        item['link'] = response.xpath("//div[@id=\"Zoom\"]/td/table/tbody/tr/td/a/@href").extract()[0]
        yield item
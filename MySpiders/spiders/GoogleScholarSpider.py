import json
import os
import time

import scrapy
from MySpiders.items import GoogleScholarItem


class GoogleScholar(scrapy.Spider):
    name = 'GoogleScholar'
    allowed_domains = ['scholar.google.com/','scholar.google.com']
    start_urls = ['https://scholar.google.com//']

    # 需要查的主题
    topics = ["neo4j"]


    def start_requests(self):
        for topic in self.topics:
            url = self.start_urls[0]
            url = url + "scholar?start=0&q=" + topic + "&hl=zh-CN&as_sdt=0,5"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        blocks = response.css(".gs_rt")
        for block in blocks:
            item = GoogleScholarItem()
            item["url"] = block.css("a::attr(href)").extract_first()
            item["title"] = block.css("a::text").extract()
            yield item
        next = response.css("td[align=left] a::attr(href)").extract()[0][1:]
        next = (self.start_urls[0] + next)
        time.sleep(10)
        yield scrapy.Request(url=next, callback=self.parse)

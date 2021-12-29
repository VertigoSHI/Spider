import json
import os

import scrapy
from MySpiders.items import GoogleScholarItem


class GoogleScholarSpider(scrapy.Spider):
    name = 'GoogleScholarSpider'
    allowed_domains = ['scholar.google.com/']
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
        next_bottom = response.xpath("/html/body/div[1]/div[11]/div[2]/div[3]/div[3]/div[2]/center/table/tbody/tr/td[12]/a/@href")[0].get_all()
        yield scrapy.Request(url=next_bottom, callback=self.start_urls)

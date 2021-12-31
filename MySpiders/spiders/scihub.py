import json
import os
import pathlib

import requests
import scrapy


class ScihubSpider(scrapy.Spider):
    name = 'scihub'
    allowed_domains = ['sci-hub.se']
    start_urls = ['http://sci-hub.se/']

    dois = []
    num = 0
    # doi 号
    doi_path = "C:/Users/VertigoSHI/Desktop/Spider/MySpiders/spiders/test.txt"
    # 下载文件夹地址
    download_path = "save"

    def readDoi(self):
        f = open(self.doi_path, "r+")
        lines = f.readlines()
        for line in lines:
            self.dois.append(line)

    def start_requests(self):
        url = self.start_urls[0]
        self.readDoi()
        for doi in self.dois:
            payload = {
                "sci-hub-plugin-check": "",
                "request": doi
            }
            yield scrapy.FormRequest(url=url, formdata=payload, method="POST")

    def parse(self, response):
        # print("---------------------")
        # print(response.text)
        # print("---------------------")
        path = pathlib.Path(self.download_path)
        if not path.exists():
            os.makedirs(self.download_path)
        pdf_embed_url = response.css('div#article embed::attr(src)').extract()[0]
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        r = requests.get(headers=headers,url=pdf_embed_url, allow_redirects=True, stream=True)
        with open(str(self.num) + ".pdf", "wb+") as f:
            for ch in r:
                f.write(ch)
                f.flush()
            f.close()
        self.num += 1

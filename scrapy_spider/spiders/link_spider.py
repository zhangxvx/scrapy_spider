import os

import scrapy
from scrapy import cmdline

from scrapy_spider.spiders import file_util

DIR_PATH = 'F:/Spider/'
LINK_PATH = 'F:/Spider/scratch.csv'


class LinkSpider(scrapy.Spider):
    name = "link_spider"

    def start_requests(self):
        urls = file_util.get_list(LINK_PATH)
        print('总数：' + str(len(urls)))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        images = response.css('#masonry div::attr(data-src)').extract()
        title = response.css('h1.post-title::text').extract_first()
        for img in images:
            yield scrapy.Request(url=img, callback=self.save, meta={'title': title})

    def save(self, response):
        path = DIR_PATH + response.meta['title']
        if not os.path.exists(path):
            os.makedirs(path)
        filename = response.url[(response.url.rfind("/") + 1):]
        file = path + '/' + filename
        if os.path.exists(file):
            return
        with open(file, 'wb') as f:
            f.write(response.body)
        print(file)


if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', 'link_spider'])

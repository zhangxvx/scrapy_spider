import os
from abc import ABC

import scrapy
from scrapy import cmdline

from scrapy_spider.spiders import file_util

DIR_PATH = 'F:/Spider/'
LINK_PATH = 'F:/Spider/scratch.csv'


class NameSpider(scrapy.Spider, ABC):
    name = "name_spider"

    def start_requests(self):
        urls = file_util.get_list(LINK_PATH)
        print('总数：' + str(len(urls)))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.person)

    def person(self, response):
        pages = set(response.css('a.page-link::attr(href)').extract())
        pages.add(response.url)
        for page in pages:
            print('page:' + page)
            yield scrapy.Request(url=page, callback=self.page, meta={'page': page}, dont_filter=True)

    def page(self, response):
        person = response.css('p.h4::text').extract_first()
        links = response.css('a.item-link::attr(href)').extract()
        for link in links:
            print(person, response.meta['page'], link)
            yield scrapy.Request(url=link, callback=self.link, meta={'person': person})

    def link(self, response):
        images = response.css('#masonry div::attr(data-src)').extract()
        title = response.css('h1.post-title::text').extract_first()
        person = response.meta['person']
        for img in images:
            yield scrapy.Request(url=img, callback=self.save, meta={'title': title, 'person': person})

    def save(self, response):
        path = '{}/{}/{}'.format(DIR_PATH, response.meta['person'], response.meta['title'])
        if not os.path.exists(path):
            os.makedirs(path)
        filename = response.url[(response.url.rfind("/") + 1):]
        filepath = '{}/{}'.format(path, filename)
        with open(filepath, 'wb') as f:
            f.write(response.body)
        print(filepath)


if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', 'name_spider'])

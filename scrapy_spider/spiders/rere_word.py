import re
from abc import ABC

import scrapy
from scrapy import cmdline

OUTPUT_PATH = '../../output/rare_word.txt'

class NameSpider(scrapy.Spider, ABC):
    name = 'rere_word'
    count = 0

    def start_requests(self):
        start_url = 'https://zidian.98zw.com/pinyin/'
        yield scrapy.Request(url=start_url, callback=self.parse_home)

    def parse_home(self, response):
        link_list = response.css('div.yingList>a[href^="/pinyin"]::attr(href)').extract()
        pinyin_list = {x for x in link_list if re.match('/pinyin/[a-z]+.html', x, 0)}

        for i in pinyin_list:
            yield scrapy.Request(url="https://zidian.98zw.com" + i, callback=self.parse_item, meta={'pinyin': i[8:-5]})

    def parse_item(self, response):
        pinyin = response.meta['pinyin']
        word_list = response.css('p.zi>a::text').extract()
        self.count += len(word_list)
        print(format('pinyin:{}. num:{}. count:{}'.format(pinyin, len(word_list), self.count)))

        res = {pinyin + ' ' + x + '\n' for x in word_list}
        with open(OUTPUT_PATH, 'a+', encoding='utf-8') as f:
            f.writelines(res)


if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', 'rere_word'])

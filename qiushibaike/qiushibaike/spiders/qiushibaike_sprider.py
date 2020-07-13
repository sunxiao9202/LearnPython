import scrapy
from scrapy.spiders import Spider

from qiushibaike.qiushibaike.items import QiushibaikeItem


class QiushiSpider(Spider):
    name = "qiushibaike"

    def start_requests(self):
        urls = [
            'https://www.qiushibaike.com/text/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content_left_div = response.xpath('// *[ @ id = "content"] / div / div[2]')
        content_list_div = content_left_div.xpath('./div')
        for content_div in content_list_div:
            item = QiushibaikeItem()
            item['author'] = content_div.xpath('./div[1]/a[2]/h2/text()').get(),
            item['content'] = content_div.xpath('./a[1]/div/span/text()').getall(),
            item['_id'] = content_div.attrib['id']
            yield item

        next_page = response.xpath('//*[@id="content"]/div/div[2]/ul/li[8]/a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse())

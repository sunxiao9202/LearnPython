import scrapy

from ImageSpider.items import ImagespiderItem


class ImgspiderSpider(scrapy.Spider):
    name = 'ImgSpider'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/archives/55.html']

    def parse(self, response):
        item = ImagespiderItem()
        imgUrls = response.css(".post img::attr(src)").extract()
        item['imgurl'] = imgUrls
        yield item
        pass

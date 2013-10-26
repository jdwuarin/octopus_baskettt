from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log

from webScraper.items import WebscraperItem


class TescoSpider(BaseSpider):
    name = 'tesco'
    allowed_domains = ["tesco.com", "secure.tesco.com"]
    start_urls = [
        "http://www.tesco.com/groceries/product/browse/default.aspx?N=4294793658&Ne=4294793660&lvl=3"
    ]

    def parse(self, response):

        #continue scraping with authenticated session...
        hxs = HtmlXPathSelector(response)
        products = hxs.select('//div[contains(@class, "desc")]')
        names = products.select('//a[contains(@href, "/groceries/Product/Details/")]/text()').extract()
        prices = products.select('//span[contains(@class, "linePrice")]/text()').extract()
        links = products.select('//a[contains(@href, "/groceries/Product/Details/")]/@href').extract()

        items = []

        for i in range(len(products)):

            item = WebscraperItem()

            item['price'] = prices[i]
            item['name']  = names[i]
            item['link'] = links[i]
            items.append(item)
        
        return items

        return

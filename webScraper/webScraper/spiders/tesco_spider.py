from scrapy.selector import Selector
#from scrapy.http import Request
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from webScraper.items import ProductItem


class Tesco_spider(CrawlSpider):
    name = 'tesco'
    allowed_domains = ["tesco.com", "secure.tesco.com"]

    start_urls = [
        "http://www.tesco.com/groceries/"
    ]

    rules = (

        #first level
        Rule (SgmlLinkExtractor(allow=("/groceries/department", ), restrict_xpaths=('//ul[@class="navigation Groceries"]',))
        , follow= True),

        #second level
        Rule (SgmlLinkExtractor(allow=("/groceries/product/browse", ), restrict_xpaths=('//div[@class="clearfix"]',))
        , callback="parse_listing_page", follow= True),

        #finally down to the parsing level
        Rule (SgmlLinkExtractor(allow=("lvl=3", ), restrict_xpaths=('//p[@class="next"]',))
        , callback="parse_listing_page", follow= True),

    )


    def parse_listing_page(self, response):

        sel = Selector(response)

        products = sel.xpath('//div[contains(@class, "desc")]')
        names = products.select('//a[contains(@href, "/groceries/Product/Details/")]/text()').extract()
        prices = products.select('//span[contains(@class, "linePrice")]/text()').extract()
        links = products.select('//a[contains(@href, "/groceries/Product/Details/")]/@href').extract()


        items = []

        for i in range(len(products)):

            if (products[i].extract().startswith('<div class="descContent')):
                continue

           # if products[i]
            # if i == 0 or i == 1:

            item = ProductItem()


            item['price'] = prices[i].replace(u'\xA3', 'GBP')
            item['name']  = names[i]
            item['link'] = links[i]
            item['productOrigin'] = 'tesco'

            if '!\r' not in names[i] and 'Cheaper alternatives' not in names[i]:
                items.append(item)
        
        return items

        return

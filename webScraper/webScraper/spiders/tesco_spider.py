from scrapy.selector import Selector
#from scrapy.http import Request
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from webScraper.items import Product_item


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

        names = self.get_good_names(sel.xpath(
            './/a[contains(@href, "/groceries/Product/Details/")]/text()').extract())
        prices = sel.xpath('//span[(@class="linePrice")]/text()').extract()
        prices_per_unit = sel.xpath('//span[(@class="linePriceAbbr")]/text()').extract()

        links = sel.xpath('//h3[contains(@class, "inBasketInfoContainer")]').xpath('.//a/@href').extract()
        external_image_links = sel.xpath('.//img[contains(@src, "img.tesco.com")]/@src').extract()
        external_ids = self.get_ids_from_links(links)


        items = []

        for i in range(len(names)):

           # if products[i]
            # if i == 0 or i == 1:

            item = Product_item()

            item['name']  = names[i]
            item['price'] = prices[i].replace(u'\xA3', 'GBP')

            item['quantity'], item['unit']  = self.get_quantity_and_unit(prices[i].replace(u'\xA3', ''), 
                prices_per_unit[i].replace(u'\xA3', ''))
            item['link'] = links[i]
            item['external_image_link'] = external_image_links[i]
            item['external_id'] = external_ids[i]
            item['product_origin'] = 'tesco'

            items.append(item)

        return items


    def get_quantity_and_unit(self, price, price_unit):
        price_unit = re.sub("[^a-zA-Z0-9/.]", "", price_unit)

        price_per_unit, unit = price_unit.split("/")
        multiplier = re.sub("[^0-9.]", "", unit)
        real_unit = re.sub("[^a-zA-Z.]", "", unit)

        try: 
            float(multiplier)
        except ValueError: 
            multiplier = 1.0

        if real_unit == "cl":
            real_unit = "ml"
            multiplier = multiplier * 10.0
        if real_unit == "l" or real_unit == "kg":
            multiplier = multiplier * 1000.0
            if real_unit == "l": 
                real_unit = "ml"
            else: 
                real_unit = "g"

        quantity = (float(price) / float(price_per_unit)) * (
            float(multiplier))

        return str(quantity), real_unit 



    def get_good_names(self, names):

        good_names =  []

        for name in names:
            if '!\r' not in name and 'Cheaper alternatives' not in name:
                good_names.append(name)

        return good_names

    def get_ids_from_links(self, links):

        external_ids = []

        for link in links:
            external_id = link.replace("/groceries/Product/Details/?id=", "")
            external_ids.append(external_id)

        return external_ids


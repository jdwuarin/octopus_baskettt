import json
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spider import BaseSpider
import re
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from octopus_groceries.models import AbstractProduct

from webScraper.items import ProductItem
from octopus_groceries.models import Supermarket


class AbstractProductProductMatchingSpider(BaseSpider):
    name = 'abs_prod_prod_match'
    tesco_base_url = "http://www.tesco.com/groceries/Product/Search/Default.aspx?searchBox="

    allowed_domains = [
        "tesco.com",

    ]

    start_urls = [
        "http://www.tesco.com"
    ]

    def parse(self, response):

        abstract_products = AbstractProduct.objects.all()
        for abstract_product in abstract_products:

            link = self.tesco_base_url + abstract_product.name.replace(" ", "+")

            tesco_request = Request(link, callback=self.parse_tesco_result_page)
            tesco_request.meta['abstract_product'] = abstract_product
            yield tesco_request

    def parse_tesco_result_page(self, response):

        sel = Selector(response)

        names = self.get_good_names(sel.xpath(
            './/a[contains(@href, "/groceries/Product/Details/")]/text()').extract())
        prices = sel.xpath('//span[(@class="linePrice")]/text()').extract()
        prices_per_unit = sel.xpath('//span[(@class="linePriceAbbr")]/text()').extract()

        links = sel.xpath('//h3[contains(@class, "inBasketInfoContainer")]').xpath('.//a/@href').extract()
        external_image_links = sel.xpath('.//img[contains(@src, "img.tesco.com")]/@src').extract()
        external_ids = self.get_ids_from_links(links)

        items = []

        rank = 1
        for i in range(len(names)):

           # if products[i]
            # if i == 0 or i == 1:

            item = ProductItem()

            item['name'] = names[i]
            item['price'] = prices[i].replace(u'\xA3', 'GBP')

            item['quantity'], item['unit'] = self.get_quantity_and_unit(prices[i].replace(u'\xA3', ''),
                                                                        prices_per_unit[i].replace(u'\xA3', ''))
            item['link'] = links[i]
            item['external_image_link'] = external_image_links[i]
            item['external_id'] = external_ids[i]
            item['supermarket'] = Supermarket.objects.get(name='tesco')
            item['matching_abstract_product'] = response.meta['abstract_product']
            item['rank'] = rank

            items.append(item)
            rank += 1

        return items

    @staticmethod
    def get_quantity_and_unit(price, price_unit):
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
            multiplier *= 10.0
        if real_unit == "l" or real_unit == "kg":
            multiplier *= 1000.0
            if real_unit == "l": 
                real_unit = "ml"
            else: 
                real_unit = "g"

        quantity = (float(price) / float(price_per_unit)) * (
            float(multiplier))

        return str(quantity), real_unit 

    @staticmethod
    def get_good_names(names):

        good_names = []

        for name in names:
            if '!\r' not in name and 'Cheaper alternatives' not in name:
                good_names.append(name)

        return good_names

    @staticmethod
    def get_ids_from_links(links):

        external_ids = []

        for link in links:
            external_id = link.replace("/groceries/Product/Details/?id=", "")
            external_ids.append(external_id)

        return external_ids

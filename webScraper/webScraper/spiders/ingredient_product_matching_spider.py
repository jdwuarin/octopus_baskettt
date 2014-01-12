import json
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider
import re
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from octopus_product.models import Ingredient

from webScraper.items import Product_item


class Ingredient_product_matching_spider(BaseSpider):
    name = 'ing_prod_match'
    tesco_base_url = "http://www.tesco.com/groceries/Product/Search/Default.aspx?searchBox="

    allowed_domains = [
        "tesco.com",

    ]

    start_urls = [
        "http://www.tesco.com"
    ]


    def parse(self, response):

        ingredients = Ingredient.objects.all()
        for ingredient in ingredients:

            link = self.tesco_base_url + ingredient.name.replace(" ", "+")

            tesco_request = Request(link, callback = self.parse_tesco_result_page)
            tesco_request.meta['ingredient'] = ingredient
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

            item = Product_item()

            item['name']  = names[i]
            item['price'] = prices[i].replace(u'\xA3', 'GBP')

            item['quantity'], item['unit']  = self.get_quantity_and_unit(prices[i].replace(u'\xA3', ''), 
                prices_per_unit[i].replace(u'\xA3', ''))
            item['link'] = links[i]
            item['external_image_link'] = external_image_links[i]
            item['external_id'] = external_ids[i]
            item['product_origin'] = 'tesco'
            item['matching_ingredient'] = response.meta['ingredient']
            item['rank'] = rank

            items.append(item)
            rank = rank + 1

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

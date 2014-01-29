from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from webScraper.items import ProductItem
from octopus_groceries.models import Supermarket


class TescoSpider(BaseSpider):
    name = 'tesco'
    allowed_domains = ["tesco.com", "secure.tesco.com"]

    start_urls = [
        "http://www.tesco.com/groceries/"
    ]

    base_url = "http://www.tesco.com"

    # rules = (
    #
    #     #first level
    #     Rule(SgmlLinkExtractor(allow=("/groceries/department", ),
    #                            restrict_xpaths=(
    #                                '//ul[@class="navigation Groceries"]',)),
    #          follow=True),
    #
    #     #second level
    #     Rule(SgmlLinkExtractor(allow=("/groceries/product/browse", ),
    #                            restrict_xpaths=('//div[@class="clearfix"]',))
    #         , callback="parse_listing_page", follow=True),
    #
    #     #finally down to the parsing level
    #     Rule(SgmlLinkExtractor(allow=("lvl=3", ),
    #                            restrict_xpaths=('//p[@class="next"]',))
    #         , callback="parse_listing_page", follow=True),
    #
    # )

    def parse(self, response):

        sel = Selector(response)
        sel = sel.xpath('//ul[contains(@class, "navigation Groceries")]')

        department_sels = sel.xpath('.//a[contains(@class, "flyout")]')

        for entry in department_sels:
            link = entry.xpath('.//@href').extract()
            request = Request(link, callback=self.parse_department)
            request.meta['department'] = entry.xpath('.//text()').extract()
            yield request

    def parse_department(self, response):

        sel = Selector(response)
        sel = sel.xpath('//div[contains(@id, "superDeptItems")]')

        sel = sel.xpath('.//ul[contains(@class, "tertNav")]')

        aisle_sels = sel.xpath('.//li')

        for entry in aisle_sels:
            link = entry.xpath('.//@href').extract()
            request = Request(link, callback=self.parse_department)
            request.meta['aisle'] = entry.xpath('.//text()').extract()
            request.meta['department'] = response.meta['department']
            yield request

    def parse_aisle(self, response):

        sel = Selector(response)
        sel = sel.xpath('//div[contains(@class, "deptNavItems")]')

        sel = sel.xpath('.//ul[contains(@class, "tertNav")]')

        category_sels = sel.xpath('.//li')

        for entry in category_sels:
            link = entry.xpath('.//@href').extract()
            request = Request(link, callback=self.parse_category)
            request.meta['category'] = entry.xpath('.//text()').extract()
            request.meta['aisle'] = response.meta['aisle']
            request.meta['department'] = response.meta['department']
            yield request

    def parse_category(self, response):

        sel = Selector(response)

        links = sel.xpath(
            '//h3[contains(@class, "inBasketInfoContainer")]').xpath(
            './/a/@href').extract()

        for link in links:
            request = Request(self.base_url + link,
                              callback=self.parse_product_page)
            request.meta['category'] = response.meta['category']
            request.meta['aisle'] = response.meta['aisle']
            request.meta['department'] = response.meta['department']
            yield request

        next_page_links = sel.xpath('//p[@class="next"]/a/@href').extract()

        if next_page_links:
            request = Request(next_page_links[0],
                              callback=self.parse_category)
            request.meta['category'] = response.meta['category']
            request.meta['aisle'] = response.meta['aisle']
            request.meta['department'] = response.meta['department']
            yield request

    def parse_product_page(self, response):

        sel = Selector(response)

        names = self.get_good_names(sel.xpath(
            './/a[contains(@href, "/groceries/Product/Details/")]/text()').extract())
        prices = sel.xpath('//span[(@class="linePrice")]/text()').extract()
        prices_per_unit = sel.xpath(
            '//span[(@class="linePriceAbbr")]/text()').extract()

        links = sel.xpath(
            '//h3[contains(@class, "inBasketInfoContainer")]').xpath(
            './/a/@href').extract()
        external_image_links = sel.xpath(
            './/img[contains(@src, "img.tesco.com")]/@src').extract()
        external_ids = self.get_ids_from_links(links)

        items = []

        for i in range(len(names)):

        # if products[i]
            # if i == 0 or i == 1:

            item = ProductItem()

            item['name'] = names[i]
            item['price'] = prices[i].replace(u'\xA3', 'GBP')

            item['quantity'], item['unit'] = self.get_quantity_and_unit(
                prices[i].replace(u'\xA3', ''),
                prices_per_unit[i].replace(u'\xA3', ''))
            item['link'] = links[i]
            item['external_image_link'] = external_image_links[i]
            item['external_id'] = external_ids[i]
            item['supermarket'] = Supermarket.objects.get(name='tesco')

            items.append(item)

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
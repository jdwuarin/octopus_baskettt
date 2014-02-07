from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from webScraper.items import ProductItem
from webScraper.product_categorization_pipeline import prod_cat_pip
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
            link = entry.xpath('.//@href').extract()[0]
            request = Request(link, callback=self.parse_department)
            request.meta['department'] = entry.xpath('.//text()').extract()[0]
            yield request

    def parse_department(self, response):

        sel = Selector(response)
        sel = sel.xpath('//div[contains(@id, "superDeptItems")]')

        sel = sel.xpath('.//ul[contains(@class, "tertNav")]')

        aisle_sels = sel.xpath('.//li')

        for entry in aisle_sels:
            link = entry.xpath('.//@href').extract()[0]
            request = Request(link, callback=self.parse_aisle)
            request.meta['aisle'] = entry.xpath('.//text()').extract()[0]
            request.meta['department'] = response.meta['department']
            yield request

    def parse_aisle(self, response):

        sel = Selector(response)
        sel = sel.xpath('//div[contains(@class, "deptNavItems")]')

        sel = sel.xpath('.//ul[contains(@class, "tertNav")]')

        category_sels = sel.xpath('.//li')

        for entry in category_sels:
            link = entry.xpath('.//@href').extract()[0]
            request = Request(link, callback=self.parse_category)
            request.meta['category'] = entry.xpath('.//text()').extract()[0]
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
            request.meta['link'] = link
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

        image_sel = sel.xpath('//div[contains(@class, "imageColumn")]')
        #we only use the first available image here
        external_image_link = image_sel.xpath('.//p/img/@src')[0].extract()
        supermarket = Supermarket.objects.get(name="tesco")
        department, aisle, category = prod_cat_pip(response, supermarket)

        product_details_sel = sel.xpath(
            '//div[@class="productDetails"]')

        name = product_details_sel.xpath('.//h1/text()').extract()[0]
        price = product_details_sel.xpath(
            './/span[@class="linePrice"]/text()').extract()[0]
        price_per_unit = product_details_sel.xpath(
            './/span[(@class="linePriceAbbr")]/text()').extract()[0]
        link = response.meta['link']
        # promotion/offer stuff
        promoBox_sel = sel.xpath('//div[@class="promoBox"]')
        promotion = promoBox_sel.xpath('.//em/text()').extract()
        external_id = link.replace("/groceries/Product/Details/?id=", "")

        # code for ingredients
        details_box_container = sel.xpath('//div[@id="detailsBox-1"]')

        ingredient_index = None

        for ii, h2 in enumerate(details_box_container.xpath(
                './/h2[not(contains(@class, "hide"))]')):
            if h2.xpath('.//text()')[0].extract() == "Ingredients":
                ingredient_index = ii

        ingredients = None
        if ingredient_index:
            ingredient_sel = details_box_container.xpath(
                './/div[@class="content"]')[ingredient_index]
            try:
                ingredients = ingredient_sel.xpath('.//p/text()').extract()[0]
            except IndexError:
                pass # this is the text starts with "<" bug
        # done with code for ingredients

        nutritionalfacts = self.get_nutritional_facts(response)


        item = ProductItem()

        item['supermarket'] = supermarket
        item['department'] = department
        item['aisle'] = aisle
        item['category'] = category
        item['price'] = price.replace(u'\xA3', 'GBP')
        item['quantity'], item['unit'] = self.get_quantity_and_unit(
            price.replace(u'\xA3', ''),
            price_per_unit.replace(u'\xA3', ''))
        item['external_image_link'] = external_image_link
        item['name'] = name
        item['link'] = link
        if promotion:
            item['promotion_flag'] = True
            item['promotion_description'] = promotion[0].replace(u'\xA3', 'GBP')
        else:
            item['promotion_flag'] = False
            item['promotion_description'] = ""
        item['external_id'] = external_id
        if ingredients:
            item['ingredients'] = ingredients
        if nutritionalfacts:
            item['nutritionalfacts'] = nutritionalfacts

        return item

    @staticmethod
    def get_quantity_and_unit(price, price_unit):
        #price per unit looks something like: 4.22/kg
        import re
        price_unit = re.sub("[^a-zA-Z0-9/.]", "", price_unit)

        price_per_unit, unit = price_unit.split("/")
        multiplier = re.sub("[^0-9.]", "", unit)
        real_unit = re.sub("[^a-zA-Z.]", "", unit)

        try:
            multiplier = float(multiplier)
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

        try:
            quantity = (float(price) / float(price_per_unit)) * (
                float(multiplier))
        except ZeroDivisionError:
            # assuming quantity = 1 in this case.
            # price per unit was returned as 0. It has been observed
            # that in this case, quantity is usually 1
            quantity = 1

        return str(quantity), real_unit

    @staticmethod
    def get_good_names(names):

        good_names = []

        for name in names:
            if '!\r' not in name and 'Cheaper alternatives' not in name:
                good_names.append(name)

        return good_names


    def get_nutritional_facts(self, response):
        sel = Selector(response)

        # nutrition_sel = None
        # potential_sels = sel.xpath('//caption')
        #
        # for xx in potential_sels:
        #     if xx.xpath('.//text()').extract()[0] == "Nutrition":
        #         nutrition_sel = xx[0]
        #         nutrition_sel = nutrition_sel.xpath('..')
        #
        # if nutrition_sel is None:
        #     return None
        #
        # # else
        #
        # headers = None
        # nutritional_facts = None

        return None
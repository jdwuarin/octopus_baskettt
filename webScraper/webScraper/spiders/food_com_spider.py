import re
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.exceptions import CloseSpider
from webScraper.items import Ingredient_item, Recipe_item


class Food_com_spider(BaseSpider):
    name = 'food.com'
    allowed_domains = ["food.com"]

    start_urls = [
        "http://www.food.com/recipe-finder/all"
    ]


    def parse(self, response):
        sel = Selector(response)
        recipe_links = sel.xpath('//a[contains(@class, "recipe-main-title")]/@href').extract()

        #for the recipes on the page
        for link in recipe_links:
            link = link + u'?mode=metric'
            recipe_request = Request(link, callback = self.parse_recipe_page)
            yield recipe_request

        #to go to the next page
        next_link_tail = sel.xpath('//a[(@rel="next")]/@href').extract()
        next_link = Food_com_spider.start_urls[0] + next_link_tail[0]
        next_request = Request(next_link, callback = self.parse)
        yield next_request

    def parse_recipe_page(self, response):

        sel = Selector(response)
        skip = False

        #first identifying num servings if it exists
        if len(sel.xpath('//p[contains(@class, "yield")]/text()').extract()) > 0:
            skip = True

        serves = sel.xpath('//option[contains(@selected, "selected")]/@value').extract()
        try:
            serves = int(serves[0])
            if serves > 4:
                skip = True
        except ValueError:
            skip = True # can't bother with anythinf that is not an int

        if skip is False:
            recipe_name = sel.xpath('//h1[contains(@class, "fn")]/text()').extract()[0]
            tags = sel.xpath('//span[contains(@itemprop, "recipeCategory")]/text()').extract()
            rating = sel.xpath('//li[contains(@class, "current-rating")]/@style').extract()[0]
            rating = float(re.sub("[^0-9.]", "", rating))
            review_count = str(sel.xpath('//a[contains(@id, "readthereview")]/text()').extract()[0])
            review_count = int(re.sub("[^0-9]", "", review_count))
            ingredient_items = []

            ingredient_information_selectors = sel.xpath('//li[contains(@class, "ingredient")]')
            for selector in ingredient_information_selectors:
                ingredient_item = Ingredient_item()

                name = selector.xpath('.//a/@href').extract()
                if len(name) is 1:
                    name = name[0]
                    name = name.replace("http://www.food.com/library/", "")
                    name =  re.sub("[^a-zA-Z]", "", name)
                    ingredient_item['name'] = name

                    quantity = selector.xpath(
                        './/span[contains(@class, "value")]/text()').extract()
                    if len(quantity) is 1:
                        quantity = quantity[0]
                        #this corrects the quantity = 0 error when using the metric system
                        try:
                            if float(quantity) == 0.0:
                                quantity = 1
                        except ValueError:
                            pass #do nothing

                        ingredient_item['quantity'] = quantity / float(serves) #to get quantities for one person

                    #we here also remove any space in the unit
                    unit = selector.xpath(
                        './/span[contains(@class, "amount")]/text()')
                    if len(unit) > 0:
                        unit = unit.extract()[0].replace(" ", "")
                        if len(unit) is 0:
                            unit = selector.xpath(
                            './/span[contains(@class, "type")]/text()').extract()
                            if len(unit) > 0:
                                unit = unit[0].replace(" ", "")
                    if len(unit) > 0:
                            ingredient_item['unit'] = unit

                    ingredient_items.append(ingredient_item)


            item = Recipe_item()
            item['name'] = recipe_name
            item['rating'] = rating
            item['review_count'] = review_count
            item['tags'] = tags
            item['ingredient_items']  = ingredient_items

            if review_count < 20:
                raise CloseSpider('done here')

            return item

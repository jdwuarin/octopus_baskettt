import re
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider
from scrapy.exceptions import CloseSpider
from webScraper.items import Ingredient_item, Recipe_item


class Food_com_spider(BaseSpider):
    name = 'food_com'
    allowed_domains = ["food.com", "mysecure.food.com"]

    start_urls = ["http://www.food.com"]

    real_start_url = "http://www.food.com/recipe-finder/all?pn="

    next_page_num = 1


    def parse(self, response):

        request = [FormRequest(url = "https://mysecure.food.com/aim/rest/login",
            formdata={
                'callbackUrl': '//www.food.com/static_files/communitytools/empty.html',
                'password': 'Test123456',
                'username': "octopus.hydra@gmail.com", }, # Test account
            callback=self.after_login
            )]

        return request



    def after_login(self, response):

        if "FAILURE" in response.body:
            print "Login failed"
            self.log("Login failed", level=log.ERROR)
            return
        else: 
            print "login successfull"
            return Request(Food_com_spider.real_start_url, callback = self.parse_listing_page)



    def parse_listing_page(self, response):

        sel = Selector(response)
        recipe_links = sel.xpath('//a[contains(@class, "recipe-main-title")]/@href').extract()

        #for the recipes on the page
        for link in recipe_links:
            link = link + u'?mode=metric'
            recipe_request = Request(link, callback = self.parse_recipe_page)
            yield recipe_request

        #to go to the next page    
        # next_link_tail = sel.xpath('//a[(@rel="next")]/@href').extract()
        Food_com_spider.next_page_num = 1 + Food_com_spider.next_page_num
        next_link = Food_com_spider.real_start_url + str(Food_com_spider.next_page_num)
        next_request = Request(next_link, callback = self.parse_listing_page)
        yield next_request


    def parse_recipe_page(self, response):

        sel = Selector(response)
        skip = False

        #first identifying num servings if it exists
        if len(sel.xpath('//p[contains(@class, "yield")]/text()').extract()) > 0:
            skip = True

        serves = self.get_cleaned_serves(sel)
        if serves is False:
            skip = True

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
                    if "http" in name: # if there is a known error on their page
                        continue
                    name =  re.sub("[^a-zA-Z-]", "", name)
                    name = name.replace("-", " ")
                    if name[-1] is " ":
                        name = name[:-1] #just remove trailing space
                    ingredient_item['name'] = name

                    quantity = self.get_cleaned_quantity(selector)
                    if not quantity is False:
                        ingredient_item['quantity'] = str(float(quantity) / float(serves)) #to get quantities for one person

                    unit = self.get_cleaned_unit(selector)
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

    def get_cleaned_serves(self, sel):
        serves = sel.xpath('//option[contains(@selected, "selected")]/@value').extract()
        if "-" in serves:
            left, sep, right = serves.rpartition("-")
            serves = (float(left) + float(right))/2.0
            return serves
        try:
            serves = int(serves[0])
            if serves > 4:
                return False
        except ValueError:
            return False # can't bother with anything that is not managed by this function

        return serves



    def get_cleaned_quantity(self, selector):

        quantity = selector.xpath(
                        './/span[contains(@class, "value")]/text()').extract()
        if len(quantity) is 1:
            quantity = quantity[0]
            if "-" in quantity:
                left, sep, right = quantity.rpartition("-")
                quantity = (float(left) + float(right))/2.0
                return str(quantity)
            else:
                try:
                    quantity = float(re.sub("[^0-9.]", "", quantity))
                    if quantity == 0.0:
                        quantity = "1"
                except ValueError:
                    pass #do nothing
                return quantity
        else:
            return False

    def get_cleaned_unit(self, selector):
        unit = selector.xpath(
            './/span[contains(@class, "amount")]/text()')
        if len(unit) > 0:
            unit = unit.extract()[0].replace(" ", "")
            if len(unit) is 0:
                unit = selector.xpath(
                './/span[contains(@class, "type")]/text()').extract()
                if len(unit) > 0:
                    unit = unit[0].replace(" ", "")

        return unit


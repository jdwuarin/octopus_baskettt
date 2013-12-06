from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider
from webScraper.spiders.food_com_level_two_spider import Food_com_level_two_spider
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor



class Food_com_spider(BaseSpider):
    name = 'food.com'
    allowed_domains = ["food.com"]

    start_urls = [
        "http://www.food.com/recipes"
    ]

    base_api_url = "http://www.food.com/rzfoodservices/web/topic/getSubdomainRecipes?slug="
    end_api_url = "&tabName=popular&pageNo="

    courses = {
        "Appetizers" : "appetizers",
        "Beverages" : "beverages",
        "Breakfasts" : "breakfast",
        "Desserts" : "desserts",
        "Lunch" : "lunch",
        "Main Dishes" : "main-dish",
        "Side Dishes" : "side-dishes"
    }

    cuisines = {
        "Chinese Recipes" : "chinese",
        "French Recipes" : "french",
        "German Recipes" : "german",
        "Indian Recipes" : "indian",
        "Italian Recipes" : "italian",
        "Mexican Recipes" : "mexican",
        "Japanese Recipes" : "japanese",
        "Southern Recipes" : "southern-united-states",
        "Spanish Recipes" : "spanish",
        "Thai Recipes" : "thai"
    }

    main_ingredients = {

        "Beans" : "beans",
        "Beef" : "beef",
        "Chicken" : "chicken",
        "Fish" : "fish",
        "Fruit" : "fruit",
        "Pasta" : "pasta",
        "Pork" : "pork",
        "Rice" : "rice",
        "Vegetables" : "vegetables",
    }

    considerations = {

        "Diabetic-Friendly" : "diabetic",
        "Gluten-Free" : "gluten-free",
        "Low Fat" : "low-fat",
        "Vegetarian" : "Vegetarian",
        "Weight Watchers" : "weight-watchers"
    }

    def parse(self, response):
        sel = Selector(response)

        #only use the sub-part that contains the food types
        sel = sel.xpath('//div[contains(@class, "more-in")]')

        food_types_sel = sel.xpath(".//ul/li/a")

        for xpath in food_types_sel:

            food_type = xpath.xpath('text()').extract()
            link = xpath.css('::attr(href)').extract()
            request = Request(link[0], callback = self.parse_food_type_page)

            request.meta['food_type'] = food_type[0]
            yield request

            # for course, api_slug in courses.iteritems():
            #     if course in food_type:
            #         request.meta['course'] = food_type
            #         yield request

            # for cuisine, api_slug in cuisines.iteritems():
            #     if cuisine in food_type:
            #         request.meta['cuisine'] = food_type
            #         yield request
            
            # for mi, api_slug in cuisines.iteritems():
            #     if mi in food_type:
            #         request.meta['main_ingredients'] = food_type
            #         yield request

            # for consideration, api_slug in considerations.iteritems():
            #     if consideration in food_type:
            #         request.meta['considerations'] = food_type
            #         yield request

            # #if I get here, this means the type could not be found
            # raise Type_not_found_exception(food_type)



    def parse_food_type_page(self, response):

        #we here parse the xml pages that do not have much to do
        #with the links.

        link_slug = ""

        if self.courses.get(response.meta['food_type']) is not None:
            link_slug = self.courses.get(response.meta['food_type'])
        elif self.cuisines.get(response.meta['food_type']) is not None:
            link_slug = self.cuisines.get(response.meta['food_type'])
        elif self.main_ingredients.get(response.meta['food_type']) is not None:
            link_slug = self.main_ingredients.get(response.meta['food_type'])
        elif self.considerations.get(response.meta['food_type']) is not None:
            link_slug = self.considerations.get(response.meta['food_type'])
        else:
            raise Type_not_found_exception(response.meta['food_type'])


        my_level_two_spider = Food_com_level_two_spider()

        for i  in range(0, 10000):



    def parse_xlm_page(self, response):
        
            if my_level_two_spider.stop is False:
                link = self.base_api_url + link_slug + self.end_api_url + str(i)
                request = Request(link, callback = my_level_two_spider.parse_xlm_page)
                request.meta['food_type'] = response.meta['food_type']
                yield request




class Type_not_found_exception(Exception):
    def __init__(self, food_type):
        self.value = food_type
    def __str__(self):
        return "could not find " + repr(self.value)

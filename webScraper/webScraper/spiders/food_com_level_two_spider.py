from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from webScraper.items import Recipe_item

class Food_com_level_two_spider(object):

    def __init__(self):
        self.stop = False


    def parse_xlm_page(self, response):

        sel = Selector(response)

        review_count = sel.xpath('recipeList/recipe/reviewCount/text()').extract()
        links = sel.xpath('recipeList/recipe/recipeUrl/text()').extract()

        if len(review_count) == 0 or review_count[0] < 400:
            self.stop = True
            return

        # for link in links:
        #     request = Request(link, callback = self.parse_recipe_page)
        #     request.meta['food_type'] = response.meta['food_type']
        #     yield request



    def parse_recipe_page(self, response):

        sel = Selector(response)
        food_type = response.meta['food_type']


        name = sel.xpath('//h1[contains(@id, "itemTitle")]/text()').extract()
        rating = sel.css('meta[itemprop*=ratingValue]::attr(content)').extract()
        review_count = sel.xpath('//meta[contains(@id, "metaReviewCount")]/@content').extract()

        ingredient_list = sel.xpath('//span[contains(@id, "lblIngName")]/text()').extract()
        quantity_list = sel.css('li[id*=liIngredient]::attr(data-grams)').extract()

        # creating a dictionary from both lists
        # output = []
        # for idx, val in enumerate(ingredient_list):
        #     output.append(dict(ingredient=val, quantity=quantity_list[idx]))

        # # creating a json from it (stringifying it)
        # ingredient_list = json.dumps(output)

        item = Recipe_item()
        item['name'] = name[0]
        item['rating'] = rating[0]
        item['review_count'] = review_count[0]
        item['ingredient_list'] = ingredient_list
        item['quantity_list'] = quantity_list

        if int(review_count[0]) < 300:
            raise CloseSpider('done here')


        return item


    def parse_listing_page(self, response):

        sel = Selector(response)

        name = sel.xpath('//h1[contains(@id, "itemTitle")]/text()').extract()
        rating = sel.css('meta[itemprop*=ratingValue]::attr(content)').extract()
        review_count = sel.xpath('//meta[contains(@id, "metaReviewCount")]/@content').extract()

        ingredient_list = sel.xpath('//span[contains(@id, "lblIngName")]/text()').extract()
        quantity_list = sel.css('li[id*=liIngredient]::attr(data-grams)').extract()

        # creating a dictionary from both lists
        # output = []
        # for idx, val in enumerate(ingredient_list):
        #     output.append(dict(ingredient=val, quantity=quantity_list[idx]))

        # # creating a json from it (stringifying it)
        # ingredient_list = json.dumps(output)

        item = Recipe_item()
        item['name'] = name[0]
        item['rating'] = rating[0]
        item['review_count'] = review_count[0]
        item['ingredient_list'] = ingredient_list
        item['quantity_list'] = quantity_list

        if int(review_count[0]) < 300:
            raise CloseSpider('done here')


        return item





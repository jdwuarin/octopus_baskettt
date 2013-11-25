import json
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from webScraper.items import RecipeItem


class All_recipes_spider(BaseSpider):
    name = 'allrecipes'
    allowed_domains = ["allrecipes.com"]

    start_urls = [
        "http://allrecipes.com/Recipes/main.aspx?Page=1&vm=l&evt19=1&p34=HR_ListView#recipes"
    ]

    def parse(self, response):
        sel = Selector(response)

        recipe_links = sel.xpath('//h3[@class="resultTitle"]')
        for selector_link in recipe_links:
            link = selector_link.css('::attr(href)').extract()[0]
            yield Request(link, callback=self.parse_listing_page)

        next_links = sel.xpath('//a[contains(@href, "/main")]')
        for l in next_links:
            for i in l.css('::text').extract():
                if "NEXT" in i:
                    link = l.css('::attr(href)').extract()[0]
                    print link
                    yield Request(link, callback = self.parse)



    def parse_listing_page(self, response):

        sel = Selector(response)

        name = sel.xpath('//h1[contains(@id, "itemTitle")]/text()').extract()
        rating = sel.css('meta[itemprop*=ratingValue]::attr(content)').extract()
        review_count = sel.xpath('//meta[contains(@id, "metaReviewCount")]/@content').extract()
        ingredient_list = sel.xpath('//span[contains(@id, "lblIngName")]/text()').extract()
        amount_list = sel.css('li[id*=liIngredient]::attr(data-grams)').extract()

        #creating a dictionary from both lists
        ingredient_list = dict(zip(ingredient_list, amount_list))
        #creating a json from it (stringifying it)
        ingredient_list = json.dumps(ingredient_list, separators=(';', ': '))

        item = RecipeItem()
        item['name'] = name
        item['rating'] = rating[0]
        item['review_count'] = review_count[0]
        item['ingredient_list'] = ingredient_list


        return item

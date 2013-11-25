# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from webScraper.items import ProductItem, RecipeItem

class WebscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class Tesco_postgres_pipeline(object):
    def process_item(self, item, spider):

        if spider.name is "tesco":
            item2 = ProductItem()
            item2 = item
            item2.save()

        return item


class all_recipes_postgres_pipeline(object):
    def process_item(self, item, spider):

        if spider.name is "allrecipes":
            item2 = RecipeItem()
            item2 = item
            item2.save()

        return item
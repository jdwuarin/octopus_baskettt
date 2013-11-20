# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from webScraper.items import ProductItem

class WebscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class PostgreSQLPipeline(object):
    def process_item(self, item, spider):

        item2 = ProductItem()
        item2 = item
        item2.save()

        return item
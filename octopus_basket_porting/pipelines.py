# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class TescoBasketPortingPipeline(object):
    def process_item(self, item, spider):

        if spider.name is "tesco_basket":
            if item['success'] == "False":
                raise DropItem("someFailure occurred")

        return item


class ProductNotFoundException(Exception):
    def __init__(self, product_id):
        self.value = product_id

    def __str__(self):
        return "could not find " + repr(self.value)

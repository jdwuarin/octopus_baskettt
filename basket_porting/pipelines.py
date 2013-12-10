# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class Tesco_basket_porting_pipeline(object):
    def process_item(self, item, spider):

        if spider.name is "tesco_basket":
            if item['success'] == "False":
                raise DropItem("someFailure occured")

        return item



class Product_not_found_exception(Exception):
    def __init__(self, product_id):
        self.value = product_id
    def __str__(self):
        return "could not find " + repr(self.value)

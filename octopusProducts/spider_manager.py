import threading
from twisted.internet import reactor, defer
from scrapy.crawler import Crawler
from scrapy import log
from scrapy.utils.project import get_project_settings
from scrapy import signals
from django.shortcuts import render
import json
from django.http import HttpResponse

from webScraper.webScraper.spiders.tesco_basket_spider import TescoBasketSpider


class Spider_manager_controller(object):

    spider_manager = None

    #creates a new one if there is none otherwise passes
    @classmethod
    def create_if_none(cls): 
        if cls.spider_manager is None:
            cls.spider_manager = Spider_manager()
        else:
            pass


    @classmethod
    def add_basket_to_port(cls, basket):
        reactor.callFromThread(cls.spider_manager.create_and_run_crawler, basket)



class Spider_manager(object):

    @classmethod
    def create_and_run_crawler(cls, basket):

        spider = TescoBasketSpider(product_details = basket.product_details, 
            loginId = basket.loginId, password = basket.password, 
            root_request = basket.request)

        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(cls.basket_created, signal = signals.spider_closed)
        crawler.signals.connect(cls.basket_error, signal = signals.spider_error)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()


    @classmethod
    def basket_created(cls, spider, reason):

        print "|||||||||||||||||||||||||||||||||||"
        print "basket created "

    def basket_error(cls, failure, response, spider):

        print "|||||||||||||||||||||||||||||||||||"
        print "basket error "




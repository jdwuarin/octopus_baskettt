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


class Spider_manager(object):


    def __init__(self):
        self.unstarted_crawlers = {}
        self.active_crawlers = {}

    def create_crawler(self, basket):

        spider = TescoBasketSpider(product_details = basket.product_details, 
            loginId = basket.loginId, password = basket.password, 
            root_request = basket.request)

        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(self.basket_created, signal = signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        self.unstarted_crawlers[basket] = crawler

        print "|||||||||||||||||||||||||||||||||||"
        print "created crawler" + str(len(self.unstarted_crawlers))


    
    def run_crawlers(self):

        print "|||||||||||||||||||||||||||||||||||"
        print "crawlers array length " + str(len(self.unstarted_crawlers))


        for x in range(len(self.unstarted_crawlers)):

            basket, crawler = self.unstarted_crawlers.popitem()
            self.active_crawlers[basket] = crawler
            crawler.start()

        print "|||||||||||||||||||||||||||||||||||"
        print "told to start them " + str(len(self.unstarted_crawlers))


    def basket_created(self, spider, reason):

        del self.active_crawlers[spider.basket]

        print "|||||||||||||||||||||||||||||||||||"
        print "basket created " + str(len(self.unstarted_crawlers))

        if len(self.active_crawlers) == 0:
            Reactor_thread.set_can_wait(True)

        # response_data = {} 
        # response_data['itemAddedToBasket'] = 'True'
        # return HttpResponse(json.dumps(response_data), content_type="application/json")

class Reactor_thread(threading.Thread):

    lock = threading.Condition()
    baskets_to_port = []
    spider_manager = Spider_manager()
    can_wait = True

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        d = defer.Deferred()
        d.addCallback(self.infinite_loop)
        reactor.callLater(0, d.callback, None)
        if not reactor.running:
            reactor.run(installSignalHandlers=False)

    @classmethod
    def infinite_loop(cls, useless_variable = None):

        while True:

            #just get the length of 
            cls.lock.acquire()
            cls.instantiate_crawlers()
            cls.lock.release()

            #then run crawlers
            cls.spider_manager.run_crawlers()


    @classmethod
    def set_can_wait(cls, can_wait):
        cls.can_wait = can_wait

    @classmethod
    def instantiate_crawlers(cls):
            if not cls.can_wait:

                print "|||||||||||||||||||||||||||||||||||"
                print "creating crawlers " 
                for basket in cls.baskets_to_port:
                    cls.spider_manager.create_crawler(basket)

                cls.baskets_to_port = []
                
            else:
                print "|||||||||||||||||||||||||||||||||||"
                print "waiting " + str(cls.can_wait)
                cls.lock.wait()


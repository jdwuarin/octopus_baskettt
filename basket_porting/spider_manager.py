from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy import signals

from basket_porting.spiders.tesco_basket_spider import Tesco_basket_spider


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

    basket_status = {}

    @classmethod
    def create_and_run_crawler(cls, basket):

        spider = Tesco_basket_spider(product_details = basket.product_details, 
            loginId = basket.loginId, password = basket.password, 
            request = basket.request, thread_manager = basket.thread_manager) 

        crawled_items = []
        dropped_items = []
        cls.basket_status[basket.request] = [crawled_items, dropped_items]
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(cls.basket_created, signal = signals.spider_closed)
        crawler.signals.connect(cls.basket_error, signal = signals.spider_error)
        crawler.signals.connect(cls.item_not_added_error, signal = signals.item_dropped)
        crawler.signals.connect(cls.item_successfully_crawled, signal = signals.item_scraped)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()


    @classmethod
    def item_successfully_crawled(cls, item, response, spider):

        cls.basket_status[spider.request][0].append(item['link'])

    @classmethod
    def item_not_added_error(cls, item, spider, exception):

        cls.basket_status[spider.request][1].append(item['link'])


    @classmethod
    def basket_created(cls, spider, reason):
        spider.thread_manager.build_response(
            cls.basket_status[spider.request][0], 
            cls.basket_status[spider.request][1])
        spider.thread_manager.lock.set() #wake up thread which should return response

        print "|||||||||||||||||||||||||||||||||||"
        print "basket created "

    @classmethod
    def basket_error(cls, failure, response, spider):

        print "|||||||||||||||||||||||||||||||||||"
        print "basket error "






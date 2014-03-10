from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy import signals

from octopus_basket_porting.spiders.tesco_basket_spider import TescoBasketSpider
from octopus_basket_porting.pipelines import BadLoginException




class SpiderManagerController(object):

    spider_manager = None

    #creates a new one if there is none otherwise passes
    @classmethod
    def create_if_none(cls): 
        if cls.spider_manager is None:
            cls.spider_manager = SpiderManager()
        else:
            pass


    @classmethod
    def add_basket_to_port(cls, basket):
        reactor.callFromThread(cls.spider_manager.create_and_run_crawler, basket)


class SpiderManager(object):

    basket_status = {}

    @classmethod
    def create_and_run_crawler(cls, basket):

        spider = TescoBasketSpider(product_details=basket.product_details,
                                   loginId=basket.login_id, password=basket.password,
                                   request=basket.request, thread_manager=basket.thread_manager)

        crawled_items = []
        dropped_items = []
        cls.basket_status[basket.request] = [crawled_items, dropped_items, ]
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(cls.basket_created, signal=signals.spider_closed)
        crawler.signals.connect(cls.basket_error, signal=signals.spider_error)
        crawler.signals.connect(cls.item_not_added_error, signal=signals.item_dropped)  # determined in pipeline
        crawler.signals.connect(cls.item_successfully_crawled, signal=signals.item_scraped)  # determined in pipeline
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()


    @classmethod
    def item_successfully_crawled(cls, item, response, spider):
        #product here is still of type [Product, quantity]
        cls.basket_status[spider.request][0].append(item['product'])

    @classmethod
    def item_not_added_error(cls, item, spider, exception):

        cls.basket_status[spider.request][1].append(item['product'])


    @classmethod
    def basket_created(cls, spider, reason):
        if spider.thread_manager.response is None:
            spider.thread_manager.build_response(
                cls.basket_status[spider.request][0],
                cls.basket_status[spider.request][1])

        spider.thread_manager.lock.set()  # wake up thread which should return response

    @classmethod
    def basket_error(cls, failure, response, spider):

        if failure.check(BadLoginException):
            spider.thread_manager.build_bad_login_response()

        else:
            print "|||||||||||||||||||||||||||||||||||"
            print "uncaught basket error "

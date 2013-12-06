from django.shortcuts import render
from webScraper.webScraper.spiders.tesco_basket_spider import TescoBasketSpider

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from scrapy.utils.project import get_project_settings
from scrapy import signals


def index(request):
    return render(request, 'products/index.html')




def spider_view(request):

    spider_manager = Spider_manager()
    #for domain in ['scrapinghub.com', 'insophia.com']:

    spider_manager.setup_crawler("http://www.tesco.com/groceries/Product/Details/?id=268768585", "1")

    spider_manager.run_reactor()

    return render(request, 'products/index.html')


class Spider_manager(object):

    def __init__(self):
        self.reactor_done_running = False

    def setup_crawler(self, link, quantity):

        spider = TescoBasketSpider(link = link, quantity = quantity)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(self.stop_reactor, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()

    def run_reactor(self):
        if not self.reactor_done_running and not reactor.running:
            reactor.run(installSignalHandlers=0)

    def stop_reactor(self):
        self.reactor_done_running = True
        reactor.stop()

from django.shortcuts import render
from webScraper.webScraper.spiders.tesco_basket_spider import TescoBasketSpider

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from scrapy.utils.project import get_project_settings
from scrapy import signals


def index(request):
	return render(request, 'products/index.html')


def setup_crawler(domain):

    spider = TescoBasketSpider(domain)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def spider_view(request):
	#for domain in ['scrapinghub.com', 'insophia.com']:
	setup_crawler("http://www.tesco.com/groceries/Product/Details/?id=268768585")
	log.start()
	reactor.run(installSignalHandlers=0)

	return render(request, 'products/index.html')

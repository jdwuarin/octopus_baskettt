from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser

class TescoBasketSpider(CrawlSpider):
    name = 'tesco_basket'
    allowed_domains = ["tesco.com", "secure.tesco.com"]

    start_urls = [
        "https://secure.tesco.com/register/"
    ]

    def __init__(self, quantity):

    	self.quantity = quantity
    	self.link = ""


    def parse(self, response):

    	# response.meta['quantity'] = 7

    	self.link = response.url

    	request = [FormRequest.from_response(response,
			formdata={'loginID': 'arnaudbenard13+test@gmail.com', 'password': 'test123'}, # Test account
			formxpath="//form[@id='fSignin']",
			callback=self.after_login)]



    	# print response.headers
    	return request

    def after_login(self, response):
    	print "logged in"

        if "Sorry" in response.body:
            return
        
        request = Request(self.link, callback = self.add_product)
        request.meta['refererUrl'] = self.link
        request.meta['quantity'] = self.quantity

       	return request

    def add_product(self, response):

    	sel = Selector(response)

    	basketId = "\"" + str.replace(str(sel.xpath('//div[contains(@class, "twoPartContainerBody")]/@id').extract()[0]),
    		"basket-", "") + "\""
    	refererUrl = "\"" + response.meta['refererUrl'] + "\""
    	quantity = "\"" + response.meta['quantity'] + "\""
    	productId = str.replace(refererUrl, "http://www.tesco.com/groceries/Product/Details/?id=", "")

    	payload = '<request basketId=' + basketId + ' view="1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" timestamp="0" referrerUrl=' + refererUrl + '><basketUpdateItems><basketUpdateItem productId=' + productId + ' qty=' + quantity + ' weight="0" currentBaseProductId="asderftg" isAlternative="false" parentBaseProductId="" basketAction=""/></basketUpdateItems></request>'

    	return Request(
            url="http://www.tesco.com/groceries/ajax/UpdateActiveBasketItems.aspx",
            method='POST',
            body= payload,
            callback=self.item_added)
    
    def item_added(self,response):
    	#sel = Selector(response)
    	#open_in_browser(response)
    	#open_in_browser(response)

    	#print sel.extract()	

    	return
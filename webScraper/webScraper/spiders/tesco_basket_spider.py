from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser

class TescoBasketSpider(CrawlSpider):
    name = 'tesco_basket'
    allowed_domains = ["tesco.com", "secure.tesco.com"]


    def __init__(self, **kw):
        print "|||||||||||||||||||||||||||||||||||"
        print "in --init--"
        self.start_url = "https://secure.tesco.com/register/"
        self.product_details = kw.get('product_details')
        self.quantity = kw.get('quantity')
        self.loginId = kw.get('loginId')
        self.password = kw.get('password')
        self.root_request = kw.get('root_request')


    def start_requests(self):
        print "|||||||||||||||||||||||||||||||||||"
        print "starting requests"
        return [Request(self.start_url, callback=self.parse)]


    def parse(self, response):

        print "|||||||||||||||||||||||||||||||||||"
        print "in parse"
    	request = [FormRequest.from_response(response,
			formdata={'loginID': self.loginId, 'password': self.password}, # Test account
			formxpath="//form[@id='fSignin']",
			callback=self.after_login)]

    	return request

    def after_login(self, response):
        if "Sorry" in response.body:
            return
        
        print "|||||||||||||||||||||||||||||||||||"
        print "logged in"
        for link in self.product_details:
            request = Request(link, callback = self.add_product)
            request.meta['link'] = link
            yield request


    def add_product(self, response):

    	sel = Selector(response)

    	basketId = "\"" + str.replace(str(sel.xpath('//div[contains(@class, "twoPartContainerBody")]/@id').extract()[0]),
    		"basket-", "") + "\""
    	refererUrl = "\"" + response.meta['link'] + "\""
    	quantity = "\"" + self.product_details[refererUrl] + "\""
    	productId = str.replace(refererUrl, "http://www.tesco.com/groceries/Product/Details/?id=", "")

    	payload = '<request basketId=' + basketId + ' view="1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" timestamp="13864398230000" referrerUrl=' + refererUrl + '><basketUpdateItems><basketUpdateItem productId=' + productId + ' qty=' + quantity + ' weight="0" currentBaseProductId="asderftg" isAlternative="false" parentBaseProductId="" basketAction=""/></basketUpdateItems></request>'

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
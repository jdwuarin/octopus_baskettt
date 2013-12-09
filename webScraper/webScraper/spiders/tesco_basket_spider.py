from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from webScraper.webScraper.items import Tesco_basket_porting_item


class TescoBasketSpider(CrawlSpider):
    name = 'tesco_basket'
    allowed_domains = ["tesco.com", "secure.tesco.com"]

    start_urls = ["https://secure.tesco.com/register/"]

    def __init__(self, **kw):
        self.start_url = "https://secure.tesco.com/register/"
        self.product_details = kw.get('product_details')
        self.quantity = kw.get('quantity')
        self.loginId = kw.get('loginId')
        self.password = kw.get('password')
        self.root_request = kw.get('root_request')


    def start_requests(self):
        return [Request(self.start_url, callback=self.parse)]


    def parse(self, response):

    	request = [FormRequest.from_response(response,
			formdata={'loginID': self.loginId, 'password': self.password}, # Test account
			formxpath="//form[@id='fSignin']",
			callback=self.after_login)]

    	return request

    def after_login(self, response):
        if "Sorry" in response.body:
            return
        
        for link in self.product_details:
            request = Request(link, callback = self.add_product)
            request.meta['link'] = link
            yield request


    def add_product(self, response):

    	sel = Selector(response)

    	basketId = "\"" + str.replace(str(sel.xpath('//div[contains(@class, "twoPartContainerBody")]/@id').extract()[0]),
    		"basket-", "") + "\""
    	refererUrl = "\"" + response.meta['link'] + "\""
    	quantity = "\"" + self.product_details[response.meta['link']] + "\""
    	productId = str.replace(refererUrl, "http://www.tesco.com/groceries/Product/Details/?id=", "")

    	payload = '<request basketId=' + basketId + ' view="1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" timestamp="13864398230000" referrerUrl=' + refererUrl + '><basketUpdateItems><basketUpdateItem productId=' + productId + ' qty=' + quantity + ' weight="0" currentBaseProductId="asderftg" isAlternative="false" parentBaseProductId="" basketAction=""/></basketUpdateItems></request>'

        request = Request(
            url="http://www.tesco.com/groceries/ajax/UpdateActiveBasketItems.aspx",
            method='POST',
            body= payload,
            callback=self.item_parsed)

        request.meta['link'] = response.meta['link'] 

    	return request
    
    def item_parsed(self,response):

        response_string = Selector(response).extract()

        item = Tesco_basket_porting_item()

        if "Failure" in response_string:
            item['success']  = "False"
        else:
            item['success'] = "True"
            
        item['link'] = response.meta['link']

        return item


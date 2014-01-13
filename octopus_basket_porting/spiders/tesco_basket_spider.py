from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from octopus_basket_porting.items import TescoBasketPortingItem


class TescoBasketSpider(CrawlSpider):
    name = 'tesco_basket'
    allowed_domains = ["tesco.com", "secure.tesco.com"]

    def __init__(self, **kw):
        self.start_url = "https://secure.tesco.com/register/"
        self.product_details = kw.get('product_details')
        self.quantity = kw.get('quantity')
        self.login_id = kw.get('loginId')
        self.password = kw.get('password')
        self.request = kw.get('request')
        self.thread_manager = kw.get('thread_manager')

    def start_requests(self):
        return [Request(self.start_url, callback=self.parse)]

    def parse(self, response):

        request = [FormRequest.from_response(response,
                                             formdata={'loginID': self.login_id, 'password': self.password},
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

        basket_id = "\"" + str.replace(str(sel.xpath(
            '//div[contains(@class, "twoPartContainerBody")]/@id').extract()[0]),
            "basket-", "") + "\""
        referer_url = "\"" + response.meta['link'] + "\""
        quantity = "\"" + self.product_details[response.meta['link']] + "\""
        product_id = str.replace(referer_url, "http://www.tesco.com/groceries/Product/Details/?id=", "")

        payload = '<request basketId=' + basket_id + (
            ' view="1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"') + (
                ' timestamp="13864398230000"') + (
                    ' referrerUrl=' + referer_url + '><basketUpdateItems><basketUpdateItem') + (
                        ' productId=' + product_id) + (
                            ' qty=' + quantity) + (
                                ' weight="0" currentBaseProductId="asderftg" isAlternative="false"') + (
                                    ' parentBaseProductId="" basketAction=""/></basketUpdateItems></request>')

        request = Request(
            url="http://www.tesco.com/groceries/ajax/UpdateActiveBasketItems.aspx",
            method='POST',
            body=payload,
            callback=self.item_parsed)

        request.meta['link'] = response.meta['link']

        yield request

    def item_parsed(self, response):

        response_string = Selector(response).extract()

        item = TescoBasketPortingItem()

        if "Failure" in response_string:
            item['success'] = "False"
        else:
            item['success'] = "True"

        item['link'] = response.meta['link']

        return item


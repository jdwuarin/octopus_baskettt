class Basket_to_port(object):

    def __init__(self, request, loginId, password, product_details):
        self.loginId = loginId
        self.password = password
        self.product_details = product_details
        self.request = request

class BasketToPort(object):

    def __init__(self, request, login_id, password,
                 product_details, thread_manager):
        self.login_id = login_id
        self.password = password
        self.product_details = product_details
        self.request = request
        self.thread_manager = thread_manager

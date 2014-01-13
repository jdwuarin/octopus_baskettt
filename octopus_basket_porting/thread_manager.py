from threading import Event


class ThreadManager(object):

    def __init__(self):
        self.lock = Event()
        self.response = None

    def wait(self, server_timeout_time):
        self.lock.wait(server_timeout_time)

    def build_response(self, successful_item_list, failed_item_list):
        self.response = {}
        self.response['Response_status'] = 'no_timeout'
        for item in successful_item_list:
            self.response[item] = "True"
        for item in failed_item_list:
            self.response[item] = "False"

    def get_response(self):
        if self.response is None:
            self.response = {}
            self.response['Response_status'] = 'server_timeout'

        return self.response

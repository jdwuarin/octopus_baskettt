from threading import Event


class ThreadManager(object):

    def __init__(self):
        self.lock = Event()
        self.response = None

    def wait(self, server_timeout_time):
        self.lock.wait(server_timeout_time)

    def build_response(self, successful_item_list, failed_item_list):
        self.response = dict()
        self.response['server_timeout'] = 'False'
        self.response['good_login'] = "True"
        for item in successful_item_list:
            self.response[item] = "True"
        for item in failed_item_list:
            self.response[item] = "False"

    def build_bad_login_response(self):
        self.response = dict()
        self.response['good_login'] = "False"
        self.response['server_timeout'] = 'False'

    def get_response(self):
        if self.response is None:
            self.response = dict()
            self.response['server_timeout'] = 'True'

        return self.response

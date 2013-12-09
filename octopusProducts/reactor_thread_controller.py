from reactor_thread import Reactor_thread


class Reactor_thread_controller(object):

    reactor_thread = None

    @classmethod
    def create_and_start_thread(cls):
        if cls.reactor_thread is None:
            cls.reactor_thread = Reactor_thread()
            cls.reactor_thread.start() #start the reactor
        else:
            pass


    @classmethod
    def add_basket_to_port(cls, basket):
        print "|||||||||||||||||||||||||||||||||||"
        print "adding item"
        cls.reactor_thread.lock.acquire()
        cls.reactor_thread.set_can_wait(False)
        cls.reactor_thread.baskets_to_port.append(basket)
        cls.reactor_thread.lock.notify() #wake up thread if waiting
        cls.reactor_thread.lock.release()
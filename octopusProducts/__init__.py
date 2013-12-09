from twisted.internet import reactor
import thread

#just starting the reactor in its own thread
def start_reactor(useless_variable = None):
    if not reactor.running:
        reactor.run(installSignalHandlers=False)

thread.start_new_thread (start_reactor, (None,))


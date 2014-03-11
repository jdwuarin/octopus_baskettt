from twisted.internet import reactor
import thread


#just starting the reactor in its own thread
def start_reactor(__ = None):
    reactor.run(installSignalHandlers=False)

if not reactor.running:
    thread.start_new_thread(start_reactor, (None,))


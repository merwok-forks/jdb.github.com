
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    # Internal
    def lineReceived(self, data):
        self.d.callback(data)
        
    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

    # public API
    def random(self): 
        def gotRandom(number):
            return int(number)
        return self.command("random?").addCallback(gotRandom)

    def classified(self): 
        return self.command("classified?")

    def notify(self):
        return self.command("notif")

    def waitNotif(self):
        self.d = defer.Deferred()
        return self.d

    def stopNotify(self):
        self.sendLine("stop_notif")
        self.d = defer.Deferred()
        return self.d

    # User code, this is actually the main()
    @defer.inlineCallbacks
    def connectionMade(self):
        print (yield self.random())
        print (yield self.classified())
        print (yield self.notify())
        print "a notif: '%s'" % (yield self.waitNotif())
        print "a second notif: '%s'" % (yield self.waitNotif())
        print (yield self.stopNotify())
        reactor.stop()

factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 6789, factory)
reactor.run()

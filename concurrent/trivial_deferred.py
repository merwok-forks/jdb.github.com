# trivial_deferred.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList
from twisted.web.client import getPage
from lxml.html import fromstring

url = 'http://twistedmatrix.com'

def title( url ):
    d = getPage( url )

    def getpage_callback( html_string ):
        print fromstring( html_string ).xpath( '/html/head/title' )[0].text
        print url

    d.addCallback( getpage_callback )    
    return d

d=DeferredList( [ title( url ) for i in range(30) ] )
d.addCallback( lambda _:reactor.stop() )

reactor.run()

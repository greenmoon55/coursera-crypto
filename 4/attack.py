import urllib2
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='


class PaddingOracle(object):
    def __init__(self, ct):
        self.iv = ct[:16]
        ct = ct[16:]
        self.ct = [ct[i: i + 16] for i in xrange(0, len(ct), len(ct) / 16)]

    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True  # good padding
            return False  # bad padding


if __name__ == "__main__":
    po = PaddingOracle('f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748'
                       'b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302'
                       '936266926ff37dbf7035d5eeb4')
    po.query(sys.argv[1])       # Issue HTTP query with the given argument

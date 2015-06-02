import urllib2
from time import sleep

TARGET = 'http://crypto-class.appspot.com/po?er='

class PaddingOracle(object):
    def __init__(self, ct):
        self.ct = []
        for i in xrange(0, len(ct), 32):
            print i
            self.ct.append(self.hex_to_byte(ct[i: i + 32]))
        self.pt = ''

    @classmethod
    def hex_to_byte(self, hexstr):
        bytes = []
        for i in range(0, len(hexstr), 2):
            bytes.append(chr(int(hexstr[i:i + 2], 16)))
        return ''.join(bytes)

    @classmethod
    def strxor(self, a, b):     # xor two strings of different lengths
        while len(a) < 16:
            a = '\0' + a
        while len(b) < 16:
            b = '\0' + b
        print a.encode('hex')
        print b.encode('hex')
        if len(a) > len(b):
            return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
        else:
            return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

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

    def _query_block(self, test_block, index):
        q = ''
        for i in range(index):
            q += self.ct[i]
        encoded_query = (q + test_block + self.ct[index + 1]).encode('hex')
        print encoded_query
        return self.query(encoded_query)

    def _get_pad(self, num):
        return str(bytearray([num] * num))

    def _generate_block(self, guess_byte, pad_num, block):
        padding = self._get_pad(pad_num)
        xor_val = self.strxor(guess_byte + b'\0' * (pad_num - 1), padding)
        print self.strxor(block, xor_val).encode('hex')
        return self.strxor(block, xor_val)

    def attack(self):
        for i in range(len(self.ct) - 2):
            block = self.ct[i]
            pt_block = ''
            for j in range(1, 17):
                for guess in """ etoanihsrdluwmycgf,bp.kv'"I-T;_HAWMSB!j?ExLCDzPJNq:YOGRFU1XK*V()Q/023548697][$@Z#%&+<=>\^`{|}~""":
                    if self._query_block(self._generate_block(guess, j, block), i):
                        s = list(block)
                        s[16 - j] = chr(ord(guess) ^ ord(s[16 - j]))
                        block = ''.join(s)
                        pt_block = guess + pt_block
                        break
            self.ct[i] = block
            self.pt += pt_block
            print self.pt.encode('hex')
            print self.pt

        # last block
        i = len(self.ct) - 2
        block = self.ct[i]
        pt_block = ''
        for j in range(1, 17):
            #for guess in """ etoanihsrdluwmycgf,bp.kv'"I-T;_HAWMSB!j?ExLCDzPJNq:YOGRFU1XK*V()Q/023548697][$@Z#%&+<=>\^`{|}~""":
            for guess in xrange(2, 256):
                guess = chr(guess)
                print pt_block.encode('hex')
                if self._query_block(self._generate_block(guess, j, block), i):
                    s = list(block)
                    s[16 - j] = chr(ord(guess) ^ ord(s[16 - j]))
                    block = ''.join(s)
                    pt_block = guess + pt_block
                    break
        self.pt += pt_block
        print self.pt.encode('hex')
        print self.pt



if __name__ == "__main__":
    po = PaddingOracle('f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748'
                       'b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302'
                       '936266926ff37dbf7035d5eeb4')
    po.attack()
    #print po._get_pad(2)
    #po.query(sys.argv[1])       # Issue HTTP query with the given argument

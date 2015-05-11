from Crypto.Cipher import AES
from Crypto.Util import Counter

k1 = '140b41b22a29beb4061bda66b6747e14'
c1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'

k2 = '140b41b22a29beb4061bda66b6747e14'
c2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'

k3 = '36f18357be4dbd77f050515c73fcf9f2'
c3 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'

k4 = '36f18357be4dbd77f050515c73fcf9f2'
c4 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'

def hex_to_byte(hexstr):
    bytes = []
    for i in range(0, len(hexstr), 2):
        bytes.append(chr(int(hexstr[i:i + 2], 16)))
    return ''.join(bytes)

obj = AES.new(hex_to_byte(k1), AES.MODE_CBC, hex_to_byte(c1)[:16])
print obj.decrypt(hex_to_byte(c1)[16:])
obj = AES.new(hex_to_byte(k2), AES.MODE_CBC, hex_to_byte(c2)[:16])
print obj.decrypt(hex_to_byte(c2)[16:])
iv = int(c3[:32], 16)
obj = AES.new(hex_to_byte(k3), AES.MODE_CTR, counter=Counter.new(128, initial_value=iv))
print obj.decrypt(hex_to_byte(c3)[16:])
iv = int(c4[:32], 16)
obj = AES.new(hex_to_byte(k4), AES.MODE_CTR, counter=Counter.new(128, initial_value=iv))
print obj.decrypt(hex_to_byte(c4)[16:])


class AESCipher:
    CBC = 1
    CTR = 2

    @staticmethod
    def _hex_to_byte(hexstr):
        bytes = []
        for i in range(0, len(hexstr), 2):
            bytes.append(chr(int(hexstr[i:i + 2], 16)))
        return ''.join(bytes)

    @staticmethod
    def _xor(a, b):
        # assert len(a) == len(b)
        res = []
        for x, y in zip(a, b):
            res.append(chr(ord(x) ^ ord(y)))
        return ''.join(res)

    def __init__(self, key):
        self.key = self._hex_to_byte(key)
        self.obj = AES.new(self.key)

    def encrypt(self, pt, iv, mode):
        pt = pt[:]
        ct = [iv]
        if mode == self.CBC:
            prev = iv
            for i in xrange(0, len(pt), 16):
                if i + 16 >= len(pt):
                    pad_size = i + 16 - len(pt)
                    for _ in xrange(pad_size):
                        pt += chr(pad_size)
                cur_pt = self._xor(pt[i: i + 16], prev)
                temp_ct = self.obj.encrypt(cur_pt)
                prev = temp_ct
                ct.append(temp_ct)
        elif mode == self.CTR:
            counter = Counter.new(128, initial_value=int(iv.encode('hex'), 16))
            for i in xrange(0, len(pt), 16):
                temp_ct = self.obj.encrypt(counter())
                temp_ct = self._xor(temp_ct, pt[i: i + 16])
                ct.append(temp_ct)
        return ''.join(ct).encode('hex')

    def decrypt(self, ct, mode):
        pt = []
        len_iv = 16
        if mode == self.CBC:
            ct = self._hex_to_byte(ct)
            for i in xrange(len_iv, len(ct), 16):
                temp_pt = self.obj.decrypt(ct[i:i + 16])
                temp_pt = self._xor(temp_pt, ct[i - 16: i])
                pt.append(temp_pt)
            pt = ''.join(pt)
            pad_size = ord(pt[-1])
            pt = pt[:len(pt) - pad_size]
        elif mode == self.CTR:
            counter = Counter.new(128, initial_value=int(ct[:32], 16))
            ct = self._hex_to_byte(ct)
            for i in xrange(len_iv, len(ct), 16):
                temp_pt = self.obj.encrypt(counter())
                temp_pt = self._xor(temp_pt, ct[i: i + 16])
                pt.append(temp_pt)
            pt = ''.join(pt)
        # import ipdb; ipdb.set_trace()
        return pt

cipher1 = AESCipher(k1)
cipher2 = AESCipher(k2)
a1 = cipher1.decrypt(c1, AESCipher.CBC)
print a1
print cipher1.encrypt(a1, hex_to_byte(c1)[:16], AESCipher.CBC)

a2 = cipher2.decrypt(c2, AESCipher.CBC)
print a2
print cipher2.decrypt(c2, AESCipher.CBC).encode('hex')
print cipher2.encrypt(a2, hex_to_byte(c2)[:16], AESCipher.CBC)

cipher3 = AESCipher(k3)
a3 = cipher3.decrypt(c3, AESCipher.CTR)
print a3
print cipher3.encrypt(a3, hex_to_byte(c3)[:16], AESCipher.CTR)

cipher4 = AESCipher(k4)
a4 = cipher4.decrypt(c4, AESCipher.CTR)
print a4
print cipher4.encrypt(a4, hex_to_byte(c4)[:16], AESCipher.CTR)

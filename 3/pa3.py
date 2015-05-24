import sys

from Crypto.Hash import SHA256

data = sys.stdin.read()
chunks, chunk_size = len(data), 1024
blocks = [data[i: i + chunk_size] for i in xrange(0, chunks, chunk_size)]

h = ''
for i in xrange(len(blocks) - 1, -1, -1):
    m = SHA256.new()
    m.update(blocks[i] + h)
    h = m.digest()
    print m.hexdigest()

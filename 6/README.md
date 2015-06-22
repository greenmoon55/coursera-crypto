Break RSA! If two primes P and Q is too close, it's easy to factor N which is the product of P and Q.

For the third question, let A = 3P + 2Q, then we can prove A = ceil(2 * (isqrt(6 * N))

Q4:

1. find p, q (from Q1)
2. find φ(N) = (p-1) * (q-1)
3. find d  (e*d = 1 mod φ(N), we have e)
4. find powmod(y,d) mod N

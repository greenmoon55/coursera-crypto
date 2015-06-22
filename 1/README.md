Given 10 OTP ciphertexts encrypted with the same key, you are asked to decrypt another ciphertext.

Method 1:

Iterate over each character(0x00, 0xFF) for each position in the key, and choose the one whose sum of probability of characters in all ciphertexts is the highest.

Method 2:

According to the hint, when a space(32) is XORed with a character in [a-zA-Z](>64), the result is an alphabet. More precisely, it is the upper case or lower case of the same letter. So XOR the ciphertexts and get the position of space, then you can get the character in the key at that position.

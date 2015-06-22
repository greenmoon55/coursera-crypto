This is my favorate programming assignment, although it took me a long time.

Padding	oracle: attacker submits ciphertext and learns if last bytes of plaintext are a valid pad

The server will return 403 for invalid pad or 404 for valid pad.

Guess from the first block to the last block and from the last char to the first char in each block, starting for xor guess xor 0x01. Then use a (02, 02) pad and so on.

To accelerate, only guess printable characters.

Note that for the last block, start from (02, 02) padding, because last byte xor guess(0x01) xor 0x01 will still be original last byte so it will always be valid.

freq = {'h': 3.834, '8': -3.665, '/': -2.951, '9': -3.708, '"': 1.68, 'y': 2.841, 'w': 2.919, '&': -6.843, 'Z': -5.745, 'a': 4.086, ':': -0.512, 'I': 1.616, 'p': 2.403, '%': -6.15, 'c': 2.82, 'u': 3.13, 'S': 0.296, '2': -3.13, '.': 2.208, '4': -3.393, 'X': -2.007, 'G': -0.69, 'e': 4.522, 'R': -0.734, '6': -3.708, 't': 4.231, 'v': 1.869, 'r': 3.709, 'x': -0.064, '\n': 3.028, 's': 3.79, ';': 0.742, '[': -4.401, 'L': -0.298, 'N': -0.474, 'i': 3.838, 'Q': -2.892, '0': -2.972, '3': -3.26, '@': -5.457, 'm': 2.874, 'U': -1.687, 'o': 4.088, '1': -1.942, "'": 1.816, '_': 0.436, '#': -6.15, 'T': 0.997, 'g': 2.788, '(': -2.253, ')': -2.253, 'A': 0.378, ',': 2.595, 'b': 2.442, '?': -0.009, 'J': -0.472, '7': -3.823, 'B': 0.236, 'D': -0.312, 'H': 0.415, 'n': 3.979, 'f': 2.724, ' ': 5.13, 'E': -0.024, '-': 1.42, 'M': 0.32, 'j': 0.078, 'd': 3.568, 'V': -2.248, 'W': 0.331, 'q': -0.497, 'Y': -0.593, 'k': 1.963, '$': -5.339, ']': -4.317, 'C': -0.308, 'l': 3.402, '*': -2.208, 'O': -0.6, 'F': -1.026, '!': 0.123, 'P': -0.355, 'K': -2.015, 'z': -0.32, '5': -3.288}
key = [0] * 1000


def freq_num(s):
    res = freq.get(chr(s), -20)
    return res


def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def read_lines():
    with open('cts.txt') as f:
        content = f.read().splitlines()
    return filter(lambda x: len(x) > 40, content)


def hex_byte_str_to_int(s):
    return int(s, 16)


# the freq is from course forum
def work_freq(lines):
    size = 83
    for i in range(size):
        max_val, n = 0, 0
        for num in range(0, 256):
            cur_val = 0
            for l in range(len(lines)):
                xor_int = num ^ int(lines[l][i*2:(i+1)*2], 16)
                cur_val += freq_num(xor_int)
            if cur_val > max_val:
                max_val, n = cur_val, num
        key[i] = n
    # Added later
    key[25] = custom_key(lines, 1, 25, 'y')
    key[0] = custom_key(lines, 10, 0, 'T')

    for line in lines:
        s = ''
        for i in range(size):
            s += chr(key[i] ^ int(line[i*2:(i+1)*2], 16))
        print s


# according to the hint
def work_space(lines):
    size = 83
    for i in range(size):
        max_val, n = 0, 0
        for num in range(0, 256):
            cur_val = 0
            for l in range(len(lines)):
                xor_int = num ^ int(lines[l][i*2:(i+1)*2], 16)
                cur_val += freq_num(xor_int)
            if cur_val > max_val:
                max_val, n = cur_val, num
            #print cur_val, num
        key[i] = n
    space_max = [0] * 1000
    for l1 in lines:
        space = [0] * 1000
        for l2 in lines:
            if l1 == l2:
                continue
            for i in xrange(0, min(len(l1), len(l2)), 2):
                byte1 = l1[i:i + 2]
                byte2 = l2[i:i + 2]
                xor = hex_byte_str_to_int(byte1) ^ hex_byte_str_to_int(byte2)
                orig_byte = xor ^ ord(' ')
                if chr(orig_byte).isalpha():
                    space[i] += 1

        for i in xrange(0, len(l1), 2):
            if space[i] > space_max[i]:
                key[i] = hex_byte_str_to_int(l1[i:i + 2]) ^ ord(' ')
                space_max[i] = space[i]
    #print key
    for line in lines:
        s = ''
        for i in xrange(0, size * 2, 2):
            s += chr(key[i] ^ int(line[i: i + 2], 16))
        print s


def custom_key(lines, l, pos, ch):
    int_result = int(lines[l][pos*2:(pos+1)*2], 16) ^ ord(ch)
    return int_result
    #return format(int_result, '0x')


def main():
    lines = read_lines()
    print lines
    work_freq(lines)
    print "\n"
    work_space(lines)


if __name__ == '__main__':
    main()

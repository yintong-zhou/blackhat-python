import sys
import socket
import threading

# We create a HEXFILTER string that contains ASCII printable characters, if one exists, or a dot (.) if such a representation doesn’t exist
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    # decoding the bytes if a byte string was passed in
    if isinstance(src, bytes):
        src = src.decode()
    
    results = list()
    for i in range(0, len(src), length):
        # we grab a piece of the string to dump and put it into the word variable
        word = str(src[i:i+length])

        # use the translate to substitute the string representation of each character for the corresponding character in the raw string
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3

        # create a new array to hold the strings, that containsthe hex value of index and the hex value of the word
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
        if show:
            for line in results:
                print(line)
        else:
            return results

# create here receive from definition
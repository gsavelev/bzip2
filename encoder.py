import math
import sys
import struct

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.encoder import HuffmanEncoder


def encode(infile):
    bwt = BWT()
    mtf = MTF()
    huff = HuffmanEncoder()

    bwt_str = bwt.transform(str(infile))
    mtf_list = mtf.transform(bwt_str)
    tree, alphabet, code = huff.encode(mtf_list)

    byte_tree = bitstring_to_bytes(tree)
    byte_alphabet = integers_to_bytes(alphabet)
    byte_code = bitstring_to_bytes(code)

    soh = chr(1)
    stx = chr(2)

    header = bytearray()
    header.extend(soh.encode())
    header.extend(struct.pack('i', len(byte_tree)))
    header.extend(struct.pack('i', len(byte_alphabet)))
    header.extend(struct.pack('i', len(byte_code)))
    header.extend(stx.encode())

    buffer = bytearray()
    buffer.extend(header)
    buffer.extend(byte_tree)
    buffer.extend(byte_alphabet)
    buffer.extend(byte_code)

    return buffer


def bitstring_to_bytes(data: str) -> bytearray:
    l = len(data)
    if l % 8 != 0:
        n_extra = math.ceil(l / 8) * 8 - l
        data += '0' * n_extra
    byte_code = bytearray()
    for i in range(0, l + n_extra, 8):
        byte_code.append(int(data[i:i + 8], 2))
    return byte_code


def integers_to_bytes(data: list) -> bytearray:
    byte_data = bytearray()
    for i in range(len(data)):
        byte_data.extend(struct.pack('i', data[i]))
    return byte_data


def main():
    infile_name = sys.argv[1]
    zipfile_name = sys.argv[2]

    try:
        with open(infile_name, 'rb') as infile:
            encoded = encode(infile.read())
    except FileNotFoundError:
        try:
            infile_name = 'data/' + infile_name
            with open(infile_name, 'rb') as infile:
                encoded = encode(infile.read())
        except FileNotFoundError:
            raise FileNotFoundError('Can not find input data [arg 1]')

    with open(zipfile_name, 'wb') as zipfile:
        zipfile.write(encoded)


if __name__ == '__main__':
    main()

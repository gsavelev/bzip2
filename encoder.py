import math
import sys

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

    byte_code = make_bytes(tree)
    byte_code.extend('\x00'.encode())  # add separator '\x00'
    byte_code.extend(bytes(alphabet))
    byte_code.extend('\x00'.encode())
    byte_code.extend(make_bytes(code))

    return byte_code


def make_bytes(bin_data):
    l = len(bin_data)
    if l % 8 != 0:
        n_extra = math.ceil(l / 8) * 8 - l
        bin_data = '0' * n_extra + bin_data
    byte_data = bytearray()
    for i in range(0, len(bin_data), 8):
        byte_data.append(int(bin_data[i:i + 8], 2))
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

import math
import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.encoder import HuffmanEncoder


def encode(infile):
    bwt = BWT()
    mtf = MTF()
    huff = HuffmanEncoder()

    # TODO test encoding (saw errors on tests)
    # bwt_str = bwt.transform(str(infile))
    # mtf_list = mtf.transform(bwt_str)
    tree, alphabet, code = huff.encode(infile)

    # FIXME I write each symbol (i.e. binary) as 1 byte
    #  use make_bytes()
    byte_code = bytearray(alphabet.encode())
    byte_code.extend('\x00'.encode())  # add separator '\x00'
    byte_code.extend(tree.encode())
    byte_code.extend('\x00'.encode())
    byte_code.extend(code.encode())

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

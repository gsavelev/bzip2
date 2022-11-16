import sys
import math
import json

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.encoder import HuffmanEncoder


def encode(infile):
    bwt = BWT()
    mtf = MTF()
    huff = HuffmanEncoder()

    # encoding
    bwt_str = bwt.transform(str(infile))
    mtf_str, mtf_table = mtf.transform(bwt_str)
    code, huff_dict = huff.encode(mtf_str)

    data = {
        'mtf_table': mtf_table,
        'huff_dict': huff_dict
    }

    byte_code = bytearray(json.dumps(data).encode())
    bits = []
    len_code = len(code)
    if len_code % 8 != 0:
        # add extra bytes to make length multiple of 8
        n_extra_bytes = math.ceil(len_code / 8) * 8 - len_code
        code = '0' * n_extra_bytes + code
    for i in range(0, len(byte_code), 8):
        bits.append(int(byte_code[i:i + 8], 2))
    bits.append(code)

    return bits


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

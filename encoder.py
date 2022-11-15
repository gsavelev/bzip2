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
    bwt_str, bwt_idx = bwt.transform(str(infile))
    mtf_str, mtf_table = mtf.transform(bwt_str)
    code, huff_dict = huff.encode(mtf_str)

    meta_data = {
        'bwt_idx': bwt_idx,
        'mtf_table': mtf_table,
        'huff_dict': huff_dict,
    }
    meta_data = json.dumps(meta_data)

    # making byte code: meta_data, leading 0, code
    byte_code = bytearray(meta_data.encode())
    len_code = len(code)
    if len_code % 8 != 0:
        # add extra bytes to make length multiple of 8
        n_extra_bytes = math.ceil(len_code / 8) * 8 - len_code
        code = '0' * n_extra_bytes + code
    for i in range(0, len_code + n_extra_bytes, 8):
        byte_code.append(int(code[i:i + 8], 2))

    return byte_code


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

import sys
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

    meta_data = {
        'mtf_table': mtf_table,
        'huff_dict': huff_dict
    }

    meta_data = json.dumps(meta_data)
    meta_bytes = bytearray(meta_data.encode())

    for i in range(0, len(code), 8):
        meta_bytes.append(int(code[i:i + 8], 2))

    return meta_bytes


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

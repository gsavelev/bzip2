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

    b_tree = bitstring_to_bytes(tree)
    b_alphabet = struct.pack('i' * len(alphabet), *alphabet)
    b_code = bitstring_to_bytes(code)

    soh = chr(1)
    stx = chr(2)

    header = bytearray()
    header.extend(soh.encode())
    header.extend(struct.pack('i' * 3,
                              len(b_tree), len(b_alphabet), len(b_code)))
    header.extend(stx.encode())

    buffer = bytearray()
    buffer.extend(header)
    buffer.extend(b_tree)
    buffer.extend(b_alphabet)
    buffer.extend(b_code)

    return buffer


def bitstring_to_bytes(s: str) -> bytearray:
    return int(s, 2).to_bytes(((len(s) + 7) // 8), byteorder=sys.byteorder)


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

import sys
import struct

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.encoder import HuffmanEncoder


def encode(infile):
    bwt = BWT()
    mtf = MTF()
    huff = HuffmanEncoder()

    # TODO treats the input file as a byte stream
    #  and remove encoding/decoding
    try:
        infile = infile.decode('utf-8')
        is_utf = True
    except UnicodeDecodeError:
        infile = infile.decode('latin-1')
        is_utf = False

    bwt_list = bwt.transform(infile)
    mtf_list = mtf.transform(bwt_list)
    tree, alphabet, code = huff.encode(mtf_list)

    b_tree = bitstring_to_bytes(tree)
    b_alphabet = struct.pack('i' * len(alphabet), *alphabet)
    b_code = bitstring_to_bytes(code)

    soh, stx = chr(1).encode(), chr(2).encode()

    header = bytearray()
    header.extend(soh)
    header.extend(struct.pack('?', is_utf))
    header.extend(struct.pack('i' * 5, len(tree), len(b_tree),
                              len(b_alphabet), len(code), len(b_code)))
    header.extend(stx)

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
    # with open('data/geo', 'rb') as infile:
    #     encoded = encode(infile.read())
    #     print(1)

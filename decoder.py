import re
import struct
import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.decoder import HuffmanDecoder


def decode(buffer: bytearray) -> bytearray:
    header = re.search(b'\x01(.+?)\x02', buffer).group(1)
    lens = [l for l in struct.iter_unpack('i', header)]
    l_tree, l_alphabet, l_code = lens[0][0], lens[1][0], lens[2][0]

    payload = buffer.split(b'\x01' + header + b'\x02')[1]
    tree_end = l_tree
    alphabet_end = l_tree + l_alphabet
    code_end = l_tree + l_alphabet + l_code
    byte_tree, byte_alphabet, byte_code = payload[:tree_end], \
                                          payload[tree_end:alphabet_end], \
                                          payload[alphabet_end:code_end]

    # TODO and decode bytearray to strings (tree, code) and to list (alphabet)
    tree = ...
    alphabet = ...
    code = ...
    print(1)

    bwt = BWT()
    mtf = MTF()
    huff = HuffmanDecoder([tree, alphabet, code])

    # TODO reverse transformations
    huff_str = huff.decode()
    mtf_list = mtf.undo_transform(huff_str)
    decoded_data = bwt.undo_transform(mtf_list)

    return decoded_data


def main():
    zipfile_name = sys.argv[1]
    outfile_name = sys.argv[2]

    try:
        with open(zipfile_name, 'rb') as zipfile:
            decoded = decode(zipfile.read())
    except FileNotFoundError:
        try:
            zipfile_name = 'data/' + zipfile_name
            with open(zipfile_name, 'rb') as zipfile:
                decoded = decode(zipfile.read())
        except FileNotFoundError:
            raise FileNotFoundError('Can not find zipfile [arg 1]')

    with open(outfile_name, 'wb') as outfile:
        outfile.write(decoded)


if __name__ == "__main__":
    # main()
    with open('bibz', 'rb') as zipfile:
        decoded = decode(zipfile.read())
        print(1)

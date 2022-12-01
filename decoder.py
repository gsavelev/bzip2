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
    b_tree, b_alphabet, b_code = payload[:tree_end],\
                                 payload[tree_end:alphabet_end], \
                                 payload[alphabet_end:code_end]

    tree = '0' + str(bin(int.from_bytes(b_tree, byteorder=sys.byteorder)))[2:]
    alphabet = [v[0] for v in struct.iter_unpack('i', b_alphabet)]
    code = '0' + str(bin(int.from_bytes(b_code, byteorder=sys.byteorder)))[2:]

    bwt = BWT()
    mtf = MTF()
    huff = HuffmanDecoder([tree, alphabet, code])

    # FIXME Huffman Decoder don't work with nums
    mtf_list = huff.decode()
    bwt_str = mtf.undo_transform(mtf_list)
    decoded_data = bwt.undo_transform(bwt_str)
    print(1)

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

import struct
import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.decoder import HuffmanDecoder


def decode(buffer: bytearray) -> bytearray:
    header = buffer[:28]

    lens = [l for l in struct.iter_unpack('i', header)]
    len_orig_tree, len_byte_tree = lens[0][0], lens[1][0]
    len_alphabet = lens[2][0]
    len_orig_code, len_byte_code = lens[3][0], lens[4][0]
    last_idx, eof = lens[5][0], lens[6][0]

    payload = buffer.split(header)[1]
    tree_end = len_byte_tree
    alphabet_end = len_byte_tree + len_alphabet
    code_end = len_byte_tree + len_alphabet + len_byte_code
    b_tree, b_alphabet, b_code = payload[:tree_end],\
                                 payload[tree_end:alphabet_end], \
                                 payload[alphabet_end:code_end]

    bin_tree = str(bin(int.from_bytes(b_tree, byteorder=sys.byteorder)))
    tree = bin_tree[2:].rjust(len_orig_tree, '0')
    alphabet = [v[0] for v in struct.iter_unpack('i', b_alphabet)]
    bin_code = str(bin(int.from_bytes(b_code, byteorder=sys.byteorder)))
    code = bin_code[2:].rjust(len_orig_code, '0')

    bwt = BWT()
    mtf = MTF()
    huff = HuffmanDecoder(tree, alphabet, code)

    mtf_list = huff.decode()
    bwt_list = mtf.undo_transform(mtf_list)
    decoded_data = bwt.undo_transform(bwt_list, last_idx, eof)

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


if __name__ == '__main__':
    main()

import re
import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.decoder import HuffmanDecoder


def decode(data: bytearray) -> bytearray:
    # TODO handle bytearray
    encoded_split = re.split('\x00', data.decode())
    # TODO bytearray to strings (tree, code) and list (alphabet)

    bwt = BWT()
    mtf = MTF()
    huff = HuffmanDecoder(encoded_split)

    # TODO do reverse transformations
    huff_str = huff.decode()
    mtf_list = mtf.undo_transform(huff_str)
    bwt_str = bwt.undo_transform(mtf_list)


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

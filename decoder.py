import re
import struct
import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.decoder import HuffmanDecoder


def decode(in_data: bytearray) -> bytearray:
    # TODO slice header
    #  then parse it
    header = re.split(r'\x01*\x02', struct.unpack('i', in_data))
    l_tree, l_alphabet, l_code = ...

    # TODO decode bytearray to strings (tree, code) and list (alphabet)
    #  https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
    data = ...

    bwt = BWT()
    mtf = MTF()
    huff = HuffmanDecoder(data)

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

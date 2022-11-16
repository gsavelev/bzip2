import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
# from huffman.encoder import HuffmanEncoder


def encode(infile):
    bwt = BWT()
    mtf = MTF()
    # huff = HuffmanEncoder()

    # encoding
    bwt_str = bwt.transform(str(infile))
    mtf_list = mtf.transform(bwt_str)
    # TODO make huff_dict binary
    # code, huff_dict = huff.encode(mtf_str)

    # TODO pass binary to file
    return bytearray(mtf_list)


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

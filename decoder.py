import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.decoder import HuffmanDecoder


def decode(zipfile):
    # TODO get data
    # data = zipfile
    huff_dict = data['huff_dict']
    mtf_table = data['mtf_table']
    code = data['code']

    bwt = BWT()
    mtf = MTF()
    huff = HuffmanDecoder(huff_dict)

    mtf_str = huff.decode(code)
    bwt_str = mtf.undo_transform(mtf_str, mtf_table)
    origin = bwt.undo_transform(bwt_str)

    return origin


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
    main()

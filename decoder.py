import re
import sys

from bwt.transformation import BWT
from mtf.transformation import MTF
from huffman.decoder import HuffmanDecoder


def decode(data: bytearray) -> bytearray:
    encoded_split = re.split('\x00', data.decode())

    huff = HuffmanDecoder(encoded_split)
    mtf = MTF()
    bwt = BWT()

    # TODO do reverse transformations
    huff_str = huff.decode()
    # mtf_list = mtf.transform(bwt_str)
    # bwt_str = bwt.transform(str(infile))

    print(1)


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
    from encoder import encode
    s = 'AAAAAABCCCCCCDDEEEEE'
    code = encode(s)
    decode(code)

import sys


def decode(zipfile):
    # TODO decode file here
    pass


def main():
    zipfile_name = sys.argv[1]
    outfile_name = sys.argv[2]

    with open(zipfile_name, 'rb') as zipfile:
        decoded_file = decode(zipfile.read())

    with open(outfile_name, 'w') as outfile:
        outfile.write(decoded_file)


if __name__ == "__main__":
    main()

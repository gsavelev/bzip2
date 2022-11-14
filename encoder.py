import sys


def encode(infile):
    # TODO encode file here
    pass


def main():
    infile_name = sys.argv[1]
    zipfile_name = sys.argv[2]

    with open(infile_name, 'rb') as infile:
        encoded_file = encode(infile.read())

    with open(zipfile_name, 'wb') as zipfile:
        zipfile.write(encoded_file)


if __name__ == "__main__":
    main()

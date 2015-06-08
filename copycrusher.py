#! /usr/bin/env python3
import os
import hashlib
import argparse
from collections import defaultdict, namedtuple

Filename = namedtuple('Filename', ['name', 'ext'])


def generate_checksum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.digest()


def is_substring(string1, string2):
    length = min(len(string1), len(string2))
    return string1[:length] == string2[:length]


def compare_filename(file1, file2):
    filename1 = Filename(os.path.splitext(file1))
    filename2 = Filename(os.path.splitext(file2))

    return is_substring(filename1.name, filename2.name) and is_substring(
        filename1.ext, filename2.ext)


def generate_checksum_dict(path):
    checksum_dict = defaultdict(list)

    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            checksum_dict[generate_checksum(
                os.path.join(root, filename))].append(filename)

    return checksum_dict


def main(path):
    from pprint import pprint
    hashes = generate_checksum_dict(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--path',
        help='This is the path you want to run the checker against')
    args = parser.parse_args()

    main(args.path)

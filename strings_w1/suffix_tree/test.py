#!/usr/bin/env python3

import sys


def find_longest_match(text1, text2):
    "".join(char1 for char1, char2 in zip(text1, text2) if char1 == char2)


if __name__ == '__main__':
    text = sys.argv[1].strip()
    subtext = sys.argv[2].strip()

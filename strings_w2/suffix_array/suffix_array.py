# python3

# Good job! (Max time used: 0.10/1.00, max memory used: 57159680/536870912.)

import sys


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    # Implement this function yourself
    suffixes = []
    for i in range(len(text)):
        suffixes.append(text[i:])
    
    len_text = len(text)
    suffix_array = []
    sorted_suffixes = sorted(suffixes)
    
    for suffix in sorted_suffixes:
        suffix_array.append(len_text - len(suffix))
    
    return suffix_array


def main():
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))


if __name__ == '__main__':
    main()
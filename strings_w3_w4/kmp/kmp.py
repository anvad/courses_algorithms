# python3

# Good job! (Max time used: 0.87/4.00, max memory used: 120274944/536870912.)

import sys


def compute_prefix_function(pattern):
    """
    Given a pattern, computes an array of integers of length = |pattern|
    Each element of the array is the longest possible border of a prefix of the pattern
    with prefix length = index of the element
    """
    s = [0] * len(pattern)
    border = 0 # holds the longest border length for the previous suffix
    w_count = 0
    for i in range(1, len(pattern)):
        print("while loop condition checked")
        while (border > 0) and (pattern[i] != pattern[border]):
            border = s[border - 1]
            w_count += 1
            print("while called.")
        if pattern[i] == pattern[border]:
            border += 1
        else:
            border = 0
        s[i] = border

    return s


def find_pattern(pattern, text):
    """
    Find all the occurrences of the pattern in the text
    and return a list of all positions in the text
    where the pattern starts in the text.
    """
    result = []
    # Implement this function yourself
    len_p = len(pattern)
    S = "$".join( [pattern, text] )
    s = compute_prefix_function(S)
    for i in range(len_p + 1, len(S)):
        if s[i] == len_p:
            result.append(i - 2 * len_p)
    return result


def main():
    pattern = sys.stdin.readline().strip()
    text = sys.stdin.readline().strip()
    result = find_pattern(pattern, text)
    print(" ".join(map(str, result)))


if __name__ == '__main__':
    main()  


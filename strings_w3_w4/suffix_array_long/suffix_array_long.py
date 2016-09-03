# python3


# Good job! (Max time used: 5.01/30.00, max memory used: 39833600/536870912.)


import sys


def convert_S_to_I(S):

    I = [-1] * len(S)

    # now to create a dictionary of alphabet
    # todo: perhaps we can extract this into own function that can dynamically extract the alphabet
    alphabet = ['$', 'A', 'C', 'G', 'T'] # sorted list of alphabet that can be extracted by parsing the string once
    atoi = {}
    for i,char in enumerate(alphabet):
        atoi[char] = i

    # now convert S to list of integers
    for i in range(len(S)):
        I[i] = atoi[S[i]]

    #print("I={}, alphabet={}".format(I, alphabet))

    return I, alphabet

def sort_characters(S, alphabet):
    """Computes order of single elements of a given list of integers, using count sort."""
    len_S = len(S)
    len_alpha = len(alphabet)
    order = [0] * len_S
    count = [0] * len_alpha

    for i in range(len_S):
        count[S[i]] += 1

    for j in range(1, len_alpha):
        count[j] = count[j] + count[j - 1] # converting the count to cumulative

    for i in range(len_S - 1, -1, -1):
        c = S[i]
        count[c] -= 1
        order[count[c]] = i

    return order


def compute_character_classes(S, order):
    len_S = len(S)
    text_class = [0] * len_S
    for i in range(1, len_S):
        if S[order[i]] != S[order[i - 1]]:
            text_class[order[i]] = text_class[order[i - 1]] + 1
        else:
            text_class[order[i]] = text_class[order[i - 1]]

    return text_class


def sort_doubled(S, L, order, text_class):
    len_S = len(S)
    count = [0] * len_S
    new_order = [0] * len_S
    for i in range(len_S):
        count[text_class[i]] += 1
    for j in range(1, len_S):
        count[j] = count[j] + count[j - 1]

    for i in range(len_S - 1, -1, -1):
        start = (order[i] - L + len_S) % len_S
        cl = text_class[start]
        count[cl] -= 1
        new_order[count[cl]] = start

    print("order after sort_doubled with L = {1} = {0}".format(new_order, L))

    return new_order


def update_class(new_order, text_class, L):
    len_new_order = len(new_order)
    new_text_class = [0] * len_new_order
    for i in range(1, len_new_order):
        cur, prev = new_order[i], new_order[i - 1]
        mid, mid_prev = (cur + L) % len_new_order, (prev + L) % len_new_order
        if (text_class[cur] != text_class[prev] or
           text_class[mid] != text_class[mid_prev]):
            new_text_class[cur] = new_text_class[prev] + 1
        else:
            new_text_class[cur] = new_text_class[prev]

    print("contents of class, after cyclic shift of length {0} = {1}".format(L, new_text_class))

    return new_text_class


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    result = []
    # Implement this function yourself
    text_integer, alphabet = convert_S_to_I(text)
    order = sort_characters(text_integer, alphabet)
    print("order after sort_characters {}".format(order))
    text_class = compute_character_classes(text_integer, order)
    print("text_class after calling compute_character_classes = {}".format(text_class))
    L = 1
    len_text = len(text)
    while L < len_text:
        order = sort_doubled(text_integer, L, order, text_class)
        text_class = update_class(order, text_class, L)
        L *= 2
    return order

def main():
    #text = sys.stdin.readline().strip()
    text = "AACGATAGCGGTAGA$"
    print(" ".join(map(str, build_suffix_array(text))))


if __name__ == '__main__':
    main()
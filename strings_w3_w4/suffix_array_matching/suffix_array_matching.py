# python3

# Good job! (Max time used: 6.70/12.00, max memory used: 23617536/536870912.) <-- using find_occurrences_2
# Good job! (Max time used: 3.42/12.00, max memory used: 23617536/536870912.) <-- using find_occurrences_3

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

    #print("order after sort_doubled with L = {1} = {0}".format(new_order, L))

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

    #print("contents of class, after cyclic shift of length {0} = {1}".format(L, new_text_class))

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
    #print("order after sort_characters {}".format(order))
    text_class = compute_character_classes(text_integer, order)
    #print("text_class after calling compute_character_classes = {}".format(text_class))
    L = 1
    len_text = len(text)
    while L < len_text:
        order = sort_doubled(text_integer, L, order, text_class)
        text_class = update_class(order, text_class, L)
        L *= 2
    return order


def find_occurrence(suffix_array, text, pattern):
    """
    Finds any one occurence of pattern in text, given the text's suffix array.
    Returns:
        index of matching suffix, in the suffix array
    """
    #print("find_occurrence")
    result = -1
    len_pattern = len(pattern)
    # implement code
    l = 0
    r = len(suffix_array) - 1
    while (l <= r):
        mid = l + (r - l) // 2 # here, mid is the index of a given suffix in the suffix array
        suffix_start = suffix_array[mid]
        suffix = text[suffix_start : suffix_start + len_pattern]
        #print("l={}, mid={}, r={}, suffix_start={}, suffix={}, pattern={}".format(l, mid, r, suffix_start, suffix, pattern))
        if suffix == pattern:
            #print("find_occurrence result for pattern {} = {}".format(pattern, mid))
            return mid # note, i am not returning the starting position of matching suffix in text. 
                       # rather, I am returning the position of the matching suffix, in the suffix_array
        elif suffix < pattern:
            l = mid + 1 # move to the right half since pattern is lexically larger than suffix
        else:
            r = mid - 1 # move the left half since pattern is lexically smaller than suffix

    #print("find_occurrence result for pattern {} = {}".format(pattern, result))
    return result # if i am here, it means no match was found


def find_occurrences_2(suffix_array, text, pattern):
    """
    Finds all occurences of pattern in text, given the text's suffix array.
    """
    #print("find_occurrences_2")
    results = []
    indices = []
    len_pattern = len(pattern)
    suffix_index = find_occurrence(suffix_array, text, pattern)
    if suffix_index == -1:
        return results # no matches were found, so return emplty list
    # now go lower and higher, till we run out of matches on either side
    indices.append(suffix_index)
    next_index = suffix_index - 1
    while next_index >= 0:
        suffix_start = suffix_array[next_index]
        suffix = text[suffix_start : suffix_start + len_pattern]
        #print("go left: next_index={}, suffix_start={}, suffix={}, pattern={}".format(next_index, suffix_start, suffix, pattern))
        if suffix == pattern:
            indices.append(next_index)
            next_index -= 1 # going left first
        else:
            break
    next_index = suffix_index + 1 # going right next
    while next_index < len(suffix_array):
        suffix_start = suffix_array[next_index]
        suffix = text[suffix_start : suffix_start + len_pattern]
        #print("go right: next_index={}, suffix_start={}, suffix={}, pattern={}".format(next_index, suffix_start, suffix, pattern))
        if suffix == pattern:
            indices.append(next_index)
            next_index += 1 # going right next
        else:
            break

    # now transform the suffix_array indices into list of starting positions in text
    for i in indices:
        results.append(suffix_array[i])
    # return list of matching suffixes, as a list of starting indices of the matching suffixes in the original text
    return results


def find_occurrences_3(suffix_array, text, pattern):
    len_pattern = len(pattern)
    min_index = 0
    max_index = len(text)
    while min_index < max_index:
        mid_index = (min_index + max_index) // 2
        suffix_start = suffix_array[mid_index]
        suffix = text[suffix_start : suffix_start + len_pattern]
        if pattern > suffix:
            min_index = mid_index + 1
        else:
            max_index = mid_index
    start = min_index

    max_index = len(text)
    while min_index < max_index:
        mid_index = (min_index + max_index) // 2
        suffix_start = suffix_array[mid_index]
        suffix = text[suffix_start : suffix_start + len_pattern]
        if pattern < suffix:
            max_index = mid_index
        else:
            min_index = mid_index + 1
    end = max_index

    results = []
    if start < end:
        #print("pattern {} found between {} and {}".format(pattern, start, end))
        for i in range(start, end):
            results.append(suffix_array[i])
    return results

def find_occurrences(text, patterns):
    occs = set()

    # write your code here
    if text[-1] != "$":
        text = "".join([text, "$"])
    suffix_array = build_suffix_array(text)
    #print("suffix_array", suffix_array)

    for pattern in patterns:
        occs.update(find_occurrences_3(suffix_array, text, pattern))

    return occs


def main():
    text = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()
    occs = find_occurrences(text, patterns)
    print(" ".join(map(str, occs)))


if __name__ == '__main__':
    main()
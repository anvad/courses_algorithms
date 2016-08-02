# python3

# Good job! (Max time used: 1.24/10.00, max memory used: 75792384/536870912.)

import sys


def make_last_to_first(first_col, last_col):
    """Given the first and last columns of a BWT transformed text, 
    returns a couple of lookup arrays, 
    mapping symbols in last column to symbols in first column."""
    
    # cycle thru each symbol in first_col, capturing a 2-tuple (first_occurence_position, number_of_occurrences)
    # initialize data for first symbol
    first_col_symbols = {}
    last_col_symbol_counts = {}
    count, first_occurrence = 0, 0
    prev_symbol = first_col[0]
    last_col_symbol_counts[prev_symbol] = 0
    for i, symbol in enumerate(first_col):
        if symbol == prev_symbol:
            count += 1
        else:
            # save the prev_symbol data
            first_col_symbols[prev_symbol] = (first_occurrence, count)
            # now initialize data for next symbol
            count = 1
            first_occurrence = i
            last_col_symbol_counts[symbol] = 0
        prev_symbol = symbol
    
    # now save the prev_symbol data
    first_col_symbols[prev_symbol] = (first_occurrence, count)

    # now cycle thru each symbol in last_col and update last_to_first array
    last_to_first = []
    for symbol in last_col:
        pos_tuple = first_col_symbols[symbol]
        pos_in_first_col = pos_tuple[0] + last_col_symbol_counts[symbol]
        last_col_symbol_counts[symbol] += 1
        last_to_first.append(pos_in_first_col)

    return last_to_first

def InverseBWT(bwt):
    # write your code here
    text = []
    last_col = bwt
    first_col = sorted(last_col) # this is now a list
    last_to_first = make_last_to_first(first_col, last_col)
    #text.append(first_col[0])
    j = 0
    for _ in range(len(bwt)):
        text.append(first_col[j])
        j = last_to_first[j]
    return "".join(reversed(text))


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(InverseBWT(bwt))
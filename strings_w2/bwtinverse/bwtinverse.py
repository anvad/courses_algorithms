# python3

# Good job! (Max time used: 1.24/10.00, max memory used: 75792384/536870912.)
# Good job! (Max time used: 0.82/10.00, max memory used: 64098304/536870912.) <-- removed some unnecessary attributes in make_last_to_first


import sys


def make_last_to_first(first_col, last_col):
    """Given the first and last columns of a BWT transformed text, 
    returns a couple of lookup arrays, 
    mapping symbols in last column to symbols in first column."""
    
    first_col_symbols = {}
    last_col_symbol_counts = {}

    # cycle thru each symbol in first_col, capturing the first occurrence of each symbol
    prev_symbol = ""
    for i, symbol in enumerate(first_col):
        if symbol != prev_symbol:
            # this is first time, this symbol appears in first_col. save the spot
            first_col_symbols[symbol] = i
            last_col_symbol_counts[symbol] = 0
        prev_symbol = symbol

    # now cycle thru each symbol in last_col and update last_to_first array
    last_to_first = [-1] * len(first_col)
    for i, symbol in enumerate(last_col):
        pos_in_first_col = first_col_symbols[symbol] + last_col_symbol_counts[symbol]
        last_col_symbol_counts[symbol] += 1
        last_to_first[i] = pos_in_first_col

    return last_to_first

def InverseBWT(bwt):
    # write your code here
    text = [None] * len(bwt)
    last_col = bwt
    first_col = sorted(last_col) # this is now a list
    last_to_first = make_last_to_first(first_col, last_col)
    j = 0
    for i in range(len(bwt) - 1, -1, -1):
        text[i] = first_col[j]
        j = last_to_first[j]
    return "".join(text)


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(InverseBWT(bwt))
# python3

# Good job! (Max time used: 4.75/24.00, max memory used: 162045952/536870912.)

import sys


def preprocess_bwt(bwt):
    """
    Preprocess the Burrows-Wheeler Transform bwt of some text
    and compute as a result:
      * starts - for each character C in bwt, starts[C] is the first position 
          of this character in the sorted array of 
          all characters of the text.
      * occ_count_before - for each character C in bwt and each position P in bwt,
          occ_count_before[C][P] is the number of occurrences of character C in bwt
          from position 0 to position P inclusive.
    """
    # Implement this function yourself

    occ_counts_before = [] # outer array index maps to symbol_id, 
                           #    inner array index will map to symbol_id
                           #    inner array value will be number of occurrences of symbol, so far

    # cycle thru each symbol in first_col, capturing the first occurrence of each symbol
    first_col = sorted(bwt)
    starts = []
    symbol_to_id = {} # maps symbol to an integer to create an enum 
    prev_symbol = ""
    symbol_id = 0
    for i, symbol in enumerate(first_col):
        if symbol != prev_symbol:
            # this is first time, this symbol appears in first_col. save the spot
            starts.append(i)
            symbol_to_id[symbol] = symbol_id
            occ_counts_before.append([0] * (len(bwt) + 1)) # initializing inner array 
            symbol_id += 1
        prev_symbol = symbol

    # now cycle thru bwt (i.e. the last_col) and update occ_counts_before
    # note that occ_counts_before has one more element in the inner array than the length of the string
    for i, symbol in enumerate(bwt):
        symbol_id = symbol_to_id[symbol]
        for symbol_id2 in symbol_to_id.values():
            occ_counts_before[symbol_id2][i+1] = occ_counts_before[symbol_id2][i]
        occ_counts_before[symbol_id][i+1] += 1

    return symbol_to_id, starts, occ_counts_before


def count_occurrences(pattern, bwt, symbol_to_id, starts, occ_counts_before):
    """
    Compute the number of occurrences of string pattern in the text
    given only Burrows-Wheeler Transform bwt of the text and additional
    information we get from the preprocessing stage - starts and occ_counts_before.
    """
    # Implement this function yourself
    top = 0
    bottom = len(bwt) - 1
    try:
        pattern = [symbol_to_id[symbol] for symbol in pattern]
    except KeyError:
        return 0
    
    while top <= bottom:
        if pattern:
            symbol_id = pattern.pop()
            top = starts[symbol_id] + occ_counts_before[symbol_id][top]
            bottom = starts[symbol_id] + occ_counts_before[symbol_id][bottom + 1] - 1
        else:
            return bottom - top + 1
    return 0
     

def main():
    bwt = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()
    # Preprocess the BWT once to get starts and occ_count_before.
    # For each pattern, we will then use these precomputed values and
    # spend only O(|pattern|) to find all occurrences of the pattern
    # in the text instead of O(|pattern| + |text|).  
    symbol_to_id, starts, occ_counts_before = preprocess_bwt(bwt)
    occurrence_counts = []
    for pattern in patterns:
        occurrence_counts.append(count_occurrences(pattern, bwt, symbol_to_id, starts, occ_counts_before))
    print(' '.join(map(str, occurrence_counts)))


if __name__ == '__main__':
    main()

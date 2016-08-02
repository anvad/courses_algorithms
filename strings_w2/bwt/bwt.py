# python3

# Good job! (Max time used: 0.02/0.50, max memory used: 9007104/536870912.)


import sys


def bwt(text):
    """Constructs Burrows–Wheeler transform."""
    bwm = [] # holds the Burrows-Wheeler matrix of given text
    for i in range(len(text)):
        bwm.append(text[i:] + text[0:i])
    bwm_sorted = sorted(bwm)
    #print(bwm_sorted)
    bwt_list = []
    for i in range(len(text)):
        bwt_list.append(bwm_sorted[i][-1])
    return "".join(bwt_list)


def main():
    text = sys.stdin.readline().strip()
    print(bwt(text))


if __name__ == '__main__':
    main()
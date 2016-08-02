#!/usr/bin/env python3

import sys


class Node():
    """Defines each node of a suffix tree. Also stores the incoming edge's label as the node's label."""
    def __init__(self,
        label_start = 0, label_length = 0, 
        node_next=None):
        if node_next == None:
            node_next = {}
        self.next = node_next
        self.label = (label_start, label_length)

def build_suffix_tree(text):
    """Using Ukonnen's algorithm to build the suffix tree."""
    suffix_tree = []

    # build T1
    suffix_tree.append(Node()) # added root node
    suffix_tree.append(Node( # added 1st node
        label_start = 0,
        label_length = 1
    ))

    # now add remaining suffixes
    for i in range(1, len(text) - 1):
        # begin phase i + 1
        for j in range(i + 1):
            # add suffixes of text[0:i]
            suffix = text[j:i]
            next_key = suffix[0] # this is the key used to navigate the "next" dictionary


    return suffix_tree


def solve(text):
    result = []
    suffix_tree = build_suffix_tree(text)
    for node in suffix_tree:
        result.append(text[node.label[0] : node.label[0] + node.label[1]])
    return result


def main():
    #text = sys.stdin.readline().strip()
    #text = "ATAAATG$"
    #text = "ACA$"
    text = "ATTCT$"
    #text = "ATGCGATGACCTGACTGA#CTCAACGTATTGGCCAGA$"
    result = build_suffix_tree(text)
    print("\n".join(result))


if __name__ == '__main__':
    main()
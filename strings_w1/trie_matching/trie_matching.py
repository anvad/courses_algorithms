#!/usr/bin/env python3

# Good job! (Max time used: 1.37/7.00, max memory used: 159744000/536870912.)

import sys

NA = -1
# here's a mapping from text/pattern alphabet to an index in the node's 'next' list
alpha_to_index = {'A':0, 'C':1, 'G':2, 'T':3}
index_to_alpha = {value:key for key,value in alpha_to_index.items()}

class Node:
    def __init__ (self):
        self.next = [NA] * 4 # '* 4' is used since there are exactly 4 possible symbols?
                             # index 0 = A, 1 = C, 2 = G, 3 = T
        self.isleaf = True

# Return the trie built from patterns
# in the form of a list of Node objects,
# e.g. {nodeObj,nodeObj}
# the nodeObj is an instance of the Node class
# amd contains all the trie edges outgoing from that node
def build_trie2(patterns):
    tree = [] # contains a list of nodes. 0th node is root node. other indices point to other nodes
    # write your code here
    # let's create the root node
    tree.append(Node())
    for pattern in patterns:
        cur_node = tree[0] # the root node
        for cur_symbol in pattern:
            next_index = alpha_to_index[cur_symbol]
            cur_node_next = cur_node.next
            if cur_node_next[next_index] != -1: # this symbol was found in current node, so go down the existing path
                cur_node = tree[cur_node_next[next_index]]
            else: # this symbol was not found in current node, so add a new node/edge to the tree, at this node
                cur_node_next[next_index] = len(tree)
                cur_node.isleaf = False
                tree.append(Node())
                cur_node = tree[-1] # now this symbol is part of tree, so go down this path
    return tree


def prefix_trie_matching(text, patterns_trie):
    node = patterns_trie[0] # root node
    i = 1
    for i, cur_symbol in enumerate(text):
        next_index = alpha_to_index[cur_symbol] # next_index is the index of cur_symbol in the .next list of the node
        next_node_index = node.next[next_index] # next_node_index is the index of the node in the trie. 
                                                # if this is -1, implies there is no match
        if node.isleaf:
            #print("pattern found '{}'".format(text[:i]))
            return text[:i] # return matched prefix of given text
        elif (next_node_index > -1): # it means we found an edge with symbol matching cur_symbol
            node = patterns_trie[next_node_index]
        else:
            return "" # no match found!
    # handling the case where the pattern matches the last character of the text
    # we are handling this separately since we get the next node only after we retrieved the last symbol from text
    if node.isleaf:
        #print("pattern found '{}'".format(text[:i+1]))
        return text[:i+1] # return matched prefix of given text
    return "" # if i am here, it means we ran out of text before we finished matching the pattern


def trie_matching(text, patterns_trie):
    results = []
    for i in range(len(text)):
        if prefix_trie_matching(text[i:], patterns_trie):
            results.append(i)
    return results

def solve(text, n, patterns):
    result = []
    # write your code here
    patterns_trie = build_trie2(patterns)
    result = trie_matching(text, patterns_trie)
    return result


def main():
    text = sys.stdin.readline().strip()
    n = int (sys.stdin.readline().strip())
    patterns = []
    for i in range(n):
        patterns += [sys.stdin.readline().strip()]

    ans = solve(text, n, patterns)

    sys.stdout.write (' '.join (map (str, ans)) + '\n')


def main2():
    text = "AAA"
    n = 1
    patterns = ["AA"]
    ans = solve(text, n, patterns)

    sys.stdout.write (' '.join (map (str, ans)) + '\n')


if __name__ == '__main__':
    main()
    #main2()
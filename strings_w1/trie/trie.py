#Uses python3

# Good job! (Max time used: 0.04/2.00, max memory used: 68153344/536870912.)


import sys

# Return the trie built from patterns
# in the form of a dictionary of dictionaries,
# e.g. {0:{'A':1,'T':2},1:{'C':3}}
# where the key of the external dictionary is
# the node ID (integer), and the internal dictionary
# contains all the trie edges outgoing from the corresponding
# node, and the keys are the letters on those edges, and the
# values are the node IDs to which these edges lead.
def build_trie(patterns):
    tree = dict()
    # write your code here
    # let's create the root node
    tree[0] = dict()
    i = 1 # this is the node ID of each node we'll add to the trie
    for pattern in patterns:
        cur_node = tree[0] # the root node
        for cur_symbol in pattern:
            if cur_symbol in cur_node: # this symbol was found in current node, so go down the existing path
                cur_node = tree[cur_node[cur_symbol]]
            else: # this symbol was not found in current node, so add a new node/edge to the tree, at this node
                cur_node[cur_symbol] = i # here i is the index of the new node
                tree[i] = dict() # attached the new node to the outer dictionary
                cur_node = tree[i] # now this symbol is part of tree, so go down this path
                i += 1
    return tree


if __name__ == '__main__':
    patterns = sys.stdin.read().split()[1:]
    tree = build_trie(patterns)
    for node in tree:
        for c in tree[node]:
            print("{}->{}:{}".format(node, tree[node][c], c))

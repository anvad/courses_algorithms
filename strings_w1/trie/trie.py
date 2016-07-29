#Uses python3

# Good job! (Max time used: 0.04/2.00, max memory used: 68153344/536870912.) <-- using dictionary
# Good job! (Max time used: 0.05/2.00, max memory used: 68145152/536870912.) <-- using Node class


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


NA = -1
# here's a mapping from text/pattern alphabet to an index in the node's 'next' list
alpha_to_index = {'A':0, 'C':1, 'G':2, 'T':3}
index_to_alpha = {value:key for key,value in alpha_to_index.items()}

class Node:
    def __init__ (self):
        self.next = [NA] * 4 # '* 4' is used since there are exactly 4 possible symbols?
                             # index 0 = A, 1 = C, 2 = G, 3 = T


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
                tree.append(Node())
                cur_node = tree[-1] # now this symbol is part of tree, so go down this path
    return tree


def main(patterns):
    #patterns = sys.stdin.read().split()[1:]
    tree = build_trie(patterns)
    for node in tree:
        for c in tree[node]:
            print("{}->{}:{}".format(node, tree[node][c], c))


def main2(patterns):
    #patterns = sys.stdin.read().split()[1:]
    tree = build_trie2(patterns)
    #from pprint import pprint as pp
    #pp(index_to_alpha)
    for index, node in enumerate(tree):
        for next_index_index, next_index in enumerate(node.next):
            if next_index > -1:
                #print("{}->{}:{}".format(index, next_index, index_to_alpha[next_index_index]))
                print("{}->{}:{}".format(index, next_index, index_to_alpha[next_index_index]))


if __name__ == '__main__':
    patterns = sys.stdin.read().split()[1:]
    #patterns = ['AT', 'AG', 'AC']
    main(patterns)
    print("-----------------------------")
    main2(patterns)
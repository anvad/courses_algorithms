# python3


# Good job! (Max time used: 3.37/10.00, max memory used: 214458368/536870912.)
# Good job! (Max time used: 3.28/10.00, max memory used: 214462464/536870912.) <- after some minor updates
# Good job! (Max time used: 3.51/10.00, max memory used: 291262464/536870912.) <- using a dict() to store the edges/child_nodes increased time and memory
# Good job! (Max time used: 3.27/10.00, max memory used: 208154624/536870912.) <- back to 2nd version + yet more minor updates


import sys


#atoi = { '$':0, 'A':1, 'C': 2, 'G':3, 'T':4 }
atoi = { '$':4, 'A':3, 'C': 2, 'G':1, 'T':0 } # using reverse order since DFS in-order traversal uses a stack and there, i want $ to pop out before T
#atoi = ['$', 'A', 'C', 'G', 'T']
#atoi = ['T', 'G', 'C', 'A', '$']

class SuffixTreeNode():
    """Defines a Suffix-Tree node."""
    def __init__(self, parent = None, children = None, string_depth = 0, edge_start = -1, edge_end = -1):
        self.parent = parent
        if children:
            self.children = children
        else:
            self.children = [None] * len(atoi) # $, A, C, G, T 
        self.string_depth = string_depth # number of symbols from start of S, to get to this node
        self.edge_start = edge_start
        self.edge_end = edge_end


def create_new_leaf(node, S, suffix_start):
    #print("creating new leaf with text {} and parent '{}'".format(S[suffix_start + node.string_depth : len(S)], S[node.edge_start : node.edge_end]))
    leaf = SuffixTreeNode(
        children = None,
        parent = node,
        string_depth = len(S) - suffix_start,
        edge_start = suffix_start + node.string_depth,
        edge_end = len(S)# - 1 # algofix: removed -1
    )
    #print("created new leaf with text {} and parent '{}'".format(S[leaf.edge_start : leaf.edge_end], S[node.edge_start : node.edge_end]))
    node.children[atoi[S[leaf.edge_start]]] = leaf # algofix: changed node.edge_start to leaf.edge_start


def break_edge(node, S, start_char, offset):
    new_leaf = node.children[atoi[start_char]] # this is the current child of the passed in node. 
                                               # This will soon become the new leaf, once we introduce mid_node
    start = new_leaf.edge_start #+ node.string_depth
    edge_mid = start + offset
    mid_char = S[edge_mid]
    mid_node = SuffixTreeNode(
        children = None,
        parent = node,
        string_depth = node.string_depth + offset,
        edge_start = start, # algofix: changed from "start + offset" to start
        edge_end = edge_mid # algofix: changed from "node.children[atoi[start_char]].edge_end" to offset
    )
    node.children[atoi[start_char]] = mid_node

    #print("broke edge {} at char {}. New mid_node is '{}' at {}:{} with depth {} and parent node '{}'".format(
    #    S[start : new_leaf.edge_end],
    #    mid_char,
    #    S[mid_node.edge_start : mid_node.edge_end],
    #    start, start + offset,
    #    mid_node.string_depth,
    #    S[node.edge_start : node.edge_end]
    #))
    
    new_leaf.edge_start = edge_mid
    new_leaf.parent = mid_node
    mid_node.children[atoi[mid_char]] = new_leaf
    
    #print("new leaf from mid_node is {} with depth {}".format(
    #    S[new_leaf.edge_start : new_leaf.edge_end],
    #    new_leaf.string_depth
    #))
    return mid_node


def stf_from_sa(S, order, lcp_array):
    lcp_array.append(0) # trick to avoid one 'if' check in each loop of the for loop
    len_S = len(S)
    root = SuffixTreeNode()
    lcp_prev = 0
    cur_node = root
    for i in range(len_S):
        suffix_start = order[i]
        #print("suffix_start={}, suffix={}".format(suffix_start, S[suffix_start:]))
        while cur_node.string_depth > lcp_prev:
            #print("while lcp_prev={}, cur_node.string_depth={}".format(lcp_prev, cur_node.string_depth))
            cur_node = cur_node.parent

        #print("lcp_prev={}, cur_node.string_depth={}".format(lcp_prev, cur_node.string_depth))
        cur_string_depth = cur_node.string_depth
        if cur_string_depth < lcp_prev:
            edge_start_char = S[order[i - 1] + cur_string_depth] # this locates the outgoing edge/child from cur_node, 
                                                                 # i.e. the edge that needs to be broken
            offset = lcp_prev - cur_string_depth # offset is the index at which to break the edge
            cur_node = break_edge(cur_node, S, edge_start_char, offset) # break_edge returns mid_node, which becomes the new cur_node

        create_new_leaf(cur_node, S, suffix_start)

        lcp_prev = lcp_array[i]
    
    return root


def suffix_array_to_suffix_tree(sa, lcp, text):
    """
    Build suffix tree of the string text given its suffix array suffix_array
    and LCP array lcp_array. Return the tree as a mapping from a node ID
    to the list of all outgoing edges of the corresponding node. The edges in the
    list must be sorted in the ascending order by the first character of the edge label.
    Root must have node ID = 0, and all other node IDs must be different
    nonnegative integers. Each edge must be represented by a tuple (node, start, end), where
        * node is the node ID of the ending node of the edge
        * start is the starting position (0-based) of the substring of text corresponding to the edge label
        * end is the first position (0-based) after the end of the substring corresponding to the edge label

    For example, if text = "ACACAA$", an edge with label "$" from root to a node with ID 1
    must be represented by a tuple (1, 6, 7). This edge must be present in the list tree[0]
    (corresponding to the root node), and it should be the first edge in the list (because
    it has the smallest first character of all edges outgoing from the root).
    """
    tree = {}
    # Implement this function yourself
    return tree


def main2():
    S = sys.stdin.readline().strip()
    sa = list(map(int, sys.stdin.readline().strip().split()))
    lcp = list(map(int, sys.stdin.readline().strip().split()))
    print(S)
    root = stf_from_sa(S, sa, lcp)
    # now do depth first traversal
    stack = []
    stack.extend((i for i in root.children if i != None))
    #print("root.children", root.children)
    while len(stack) > 0:
        node = stack.pop()
        #print("node.children", node.children)
        print(node.edge_start, node.edge_end)
        #for child in node.children:
        #    stack.append(child)
        stack.extend((i for i in node.children if i != None))


def main():
    text = sys.stdin.readline().strip()
    sa = list(map(int, sys.stdin.readline().strip().split()))
    lcp = list(map(int, sys.stdin.readline().strip().split()))
    print(text)
    # Build the suffix tree and get a mapping from 
    # suffix tree node ID to the list of outgoing Edges.
    tree = suffix_array_to_suffix_tree(sa, lcp, text)
    """
    Output the edges of the suffix tree in the required order.
    Note that we use here the contract that the root of the tree
    will have node ID = 0 and that each vector of outgoing edges
    will be sorted by the first character of the corresponding edge label.
    
    The following code avoids recursion to avoid stack overflow issues.
    It uses two stacks to convert recursive function to a while loop.
    This code is an equivalent of 
    
        OutputEdges(tree, 0);
    
    for the following _recursive_ function OutputEdges:
    
    def OutputEdges(tree, node_id):
        edges = tree[node_id]
        for edge in edges:
            print("%d %d" % (edge[1], edge[2]))
            OutputEdges(tree, edge[0]);
    
    """
    stack = [(0, 0)]
    result_edges = []
    while len(stack) > 0:
        (node, edge_index) = stack[-1]
        stack.pop()
        if not node in tree:
            continue
        edges = tree[node]
        if edge_index + 1 < len(edges):
            stack.append((node, edge_index + 1))
        print("%d %d" % (edges[edge_index][1], edges[edge_index][2]))
        stack.append((edges[edge_index][0], 0))


if __name__ == '__main__':
    main2()
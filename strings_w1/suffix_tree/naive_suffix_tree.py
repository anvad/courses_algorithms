# python3
import sys

# the trie or tree is a directed graph with a root
# so, why not store is as an adjacency list?
# we'll have a master list of nodes. index 0 points to root node. all other indices point to other nodes
# each node can have up to len(alphabet) children. In our case, the alphabet is only 4 chars long
# so, we can keep the "next" list from Node class, from previous assignment
# but once we form a tree, we could have edges with longer labels (i.e. more than one char long)
# in such cases, the next list will point to first char of the label for the edge to the next node
# e.g. string ACA$
# we'll start with a min. of 2 nodes: 
#    root node (node0) with 
#        label: ACA$ => (0,4)
#        next:  [1, -1, -1, -1]
#        PatternEnd: -1
#    node 1 with
#        label: "" => (x,-1 or len_suffix) # -1 or len_suffix as the 2nd element of the lable tuple implies leaf node
#        next: [-1, -1, -1, -1] # perhaps we can omit adding this in the initializer?
# then, we'll look at next suffix CA$
#    check if root node of trie has a non-negative next for suffix[0] (i.e. 'C'), if so, traverse it, till we get to leaf
#    if not, then add node 2 with
#        label: CA$ => (1,-1) #indicates this is leaf node
# then, we'll check next suffix A$
#   traversing from root, we found A is part of node 1 and node 1 is a leaf.
#   since leaf label ACA$ does not match $ (this is the remaining portion of suffix as we traverse), 
#       we'll split node1 (i.e) modify it's props and create 2 new nodes node3 and node4 to hold remamining portion of suffix
#    node1
#        label: A => (0,1) 1 because only that part matched pattern A$. in fact, this will always be one, when we split
#        next: [-1, 3, -1, -1, 4]
#    node3
#        label: CA$ => (1, -1)
#    node4
#        label: $ => (3, -1)


NA = -1
# here's a mapping from text/pattern alphabet to an index in the node's 'next' list
alpha_to_index = {'A':0, 'C':1, 'G':2, 'T':3, '$':4}
index_to_alpha = {value:key for key,value in alpha_to_index.items()}


class Node:
    def __init__ (self):
        self.next = [NA] * len(alpha_to_index)
        self.patternEnd = False
        #self.isleaf = True


# Return the trie built from patterns
# in the form of a list of Node objects,
# e.g. {nodeObj,nodeObj}
# the nodeObj is an instance of the Node class
# amd contains all the trie edges outgoing from that node
# extended to handle cases where one of the patterns is a prefix of another pattern
def build_suffix_trie(text):
    trie = [] # contains a list of nodes. 0th node is root node. other indices point to other nodes
    # write your code here
    # let's create the root node
    trie.append(Node())
    for i in range(len(text)):
        pattern = text[i:]
        cur_node = trie[0] # the root node
        for cur_symbol in pattern:
            next_index = alpha_to_index[cur_symbol]
            cur_node_next = cur_node.next
            if cur_node_next[next_index] != -1: # this symbol was found in current node, so go down the existing path
                cur_node = trie[cur_node_next[next_index]]
            else: # this symbol was not found in current node, so add a new node/edge to the tree, at this node
                cur_node_next[next_index] = len(trie)
                #cur_node.isleaf = False
                trie.append(Node())
                cur_node = trie[-1] # now this symbol is part of tree, so go down this path
        # now we've explored this pattern, so let's set the patternEnd flag
        cur_node.patternEnd = True
        cur_node.startIndex = i # this is the startIndex of the text suffix that ends at this leaf node
    return trie


def compress_trie(trie):
    tree = {}
    # now traverse the trie using DFS, and for each node that has only one outgoing edge, 
    #   remove it
    #   update the child node's label by concatenating this node's label with the child's label
    # right now labels are stored as positional data in node.next list - i.e. as labels on outgoing edges
    # we need to store it on the node itself, as data from incoming edge, since we'll always have only one incoming edge
    
    stack = [] # using a list as a stack to do non-recursive DFS
    tree[0] = trie[0]
    trie[0].label = ""
    stack.append( (0, trie[0]) )
    label = ""
    while len(stack) > 0:
        node_index, node = stack.pop()
        if label == "":
            label = node.label
            start_index = node_index
        num_outgoing_edges = 0
        for next_index_index, next_index in enumerate(node.next):
            if next_index > -1:
                child_node = trie[next_index]
                outgoing_edge_label = index_to_alpha[next_index_index]
                child_node.label = outgoing_edge_label
                stack.append( (next_index, child_node) )
                num_outgoing_edges += 1
        if num_outgoing_edges == 1:
            label += outgoing_edge_label
        else:
            # we've reached the end of a chain (or reached a node with multiple outgoing edges), so consolidate
            node_to_keep = trie[start_index]
            node_to_keep.next = trie[node_index].next # we'll need to retain pointers to remaining nodes in chain
            node_to_keep.label = label
            tree[start_index] = node_to_keep # add this node to the tree
            #print("start-end:label: {}-{}:{}".format(start_index, node_index, label))
            label = ""
    return tree


def print_trie(trie):
    for index, node in enumerate(trie):
        for next_index_index, next_index in enumerate(node.next):
            if next_index > -1:
                print("{}->{}:{}".format(index, next_index, index_to_alpha[next_index_index]))


def print_tree(tree):
    for index, node in tree.items():
        print("{}-{}:{}".format(index, node.next, node.label))


def build_suffix_tree(text):
    """
    Build a suffix tree of the string text and return a list
    with all of the labels of its edges (the corresponding 
    substrings of the text) in any order.
    """
    result = []
    # Implement this function yourself
    # loop thru each suffix and add it to the suffix trie
    suffix_trie = build_suffix_trie(text)
    #print_trie(suffix_trie)
    suffix_tree = compress_trie(suffix_trie)
    #print_tree(suffix_tree)

    # now append all labels to result
    #for index, node in suffix_tree.items():
    #    if node.label: #eliminating the empty label on root node in the result list
    #        result.append(node.label)

    # replaced the above code with a generator comprehension :)
    result = (node.label for node in suffix_tree.values() if node.label)

    return result


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    #text = "ACA$"
    result = build_suffix_tree(text)
    print("\n".join(result))
# python3

# Good job! (Max time used: 1.09/10.00, max memory used: 55156736/536870912.) <- global text object
# Good job! (Max time used: 1.15/10.00, max memory used: 36139008/536870912.) <- text object passed as explicit are to functions

import sys

# the trie or tree is a directed graph with a root
# so, why not store is as an adjacency list of nodes?
# we'll have a master list of nodes. index 0 points to root node. all other indices point to other nodes
# but once we form a tree, we could have edges with longer labels (i.e. more than one char long)
# also, we'll store label start-index and length, rather than actual text, to save memory
# in such cases, the next list will point to first char of the label for the edge to the next node
# the label on a node, really belongs to the incoming edge. 
#    Since, in our case, we'll only ever have one incoming edge on any given node, 
#    it was easier to store the label on the node, rather than create explicit edge objects 
# e.g. process string ACA$
# we'll start with 1 node and look at suffix ACA$: 
#    root node (node0) with 
#        label: "" => (0,0)
#        next:  {'A':1}
#    node 1 with
#        label: "ACA$" => (x,-1 or len_suffix) # -1 or len_suffix as the 2nd element of the lable tuple implies leaf node
#        next: {}
# then, we'll look at next suffix CA$, etc.


class Node:
    """Captures the details of a node in the suffix tree."""
    def __init__ (self, node_next, label_start=0, label_length=0):
        self.next = node_next # key = first symbol in label, value = index in tree
        self.label = (label_start, label_length) # startIndex, length in original text


# todo: remove dependency on global text object
def add_child(text, tree, parent, label_start, label_length, node_next):
    len_tree = len(tree)
    child = Node(node_next, label_start, label_length)

    child_symbol = text[label_start]
    if child_symbol in parent.next:
        print("parent node [{}] already has a child [{}] with symbol {} but still adding child [{}]" \
            .format(parent.index, parent.next[child_symbol], child_symbol, len_tree))
        tree.append(child)
        print_tree(tree, text)
        sys.exit()
    parent.next[child_symbol] = len_tree
    tree.append(child)


def add_pattern_to_tree(tree, text, pattern, i):
    """Digests given pattern and adds nodes to given suffix tree."""

    # starting from root node, traverse path, add new node, or split existing node in to two, then return
    #print("adding pattern {}".format(pattern))
    node = tree[0] # start at root node
    while True:
        symbol = pattern[0] # get the first char of pattern
        if symbol in node.next:
            # implies this node has a child whose label starts with symbol, so pursue that path

            node = tree[node.next[symbol]] # immediately move to the matching node
            node_label = node.label
            start, length = node_label

            # get longest prefix match between given pattern and label; 
            #   Note: may need to shorten pattern as we go down the tree
            length_matched = 0
            for char1, char2 in zip(pattern, text[start : start + length]):
                if char1 == char2:
                    length_matched += 1
                else:
                    break

            if length_matched == length:
                pattern = pattern[length_matched:] # we shorten the pattern to search for, since 
                                                   # part of it's already in the tree
                i += length_matched # and we also need to advance the start index of label we'll attach
                #print("chopped pattern to '{}' on node [{}]".format(pattern, node.index))
                if not pattern:
                    print("somehow chopped down pattern to empty string")
                    print_tree(tree, text)
                    sys.exit()
                continue

            # if i am here, it implies pattern and current node's incoming edge's label matched partially
            # so, we have to add two children
            # child1 will have label's remaining part (i.e. the part that did not match)
            # child2 will have the pattern's remaining part
            # if current node already had children, then these children will now belong to child1 

            if node.next: # implies this node has children!
                child1_node_next = node.next
                node.next = {} # re-assigning node.next to new empty dictionary
            else:
                child1_node_next = {}

            # add first child
            add_child(text, tree, node, 
                label_start = start + length_matched, 
                label_length = length - length_matched,
                node_next = child1_node_next)

            # add second child
            add_child(text, tree, node, 
                label_start = i + length_matched, 
                label_length = len(pattern) - length_matched,
                node_next = {})

            # update this node's label
            node.label = (start, length_matched)

            return
        else:
            # implies we'll add a new child node since none exists with this symbol
            # also update current node's next dictionary, to point to this node, for the current symbol
            add_child(text, tree, node,
                label_start = i,
                label_length = len(pattern),
                node_next = {})
            return


def print_tree(tree, text):
    for index, node in enumerate(tree):
        print("{}-{}:{}".format(index, node.next, text[node.label[0] : node.label[0] + node.label[1]]))


def build_suffix_tree(text):
    """
    Build a suffix tree of the string text and return a list
    with all of the labels of its edges (the corresponding 
    substrings of the text) in any order.
    """
    result = []
    # Implement this function yourself
    suffix_tree = []

    # adding root node first, with original text as the first suffix
    root_node = Node(node_next={})
    suffix_tree.append(root_node)

    # now adding each suffix pattern to the tree
    for i in range(len(text)):
        pattern = text[i:]
        # now traverse tree, adding new node, or splitting existing node
        add_pattern_to_tree(suffix_tree, text, pattern, i)

    # using generator comprehension :)
    labels = (node.label for node in suffix_tree)
    result = (text[start : start + length] for start, length in labels if length)

    #print_tree(suffix_tree, text)

    return result


def main():
    text = sys.stdin.readline().strip()
    #text = "ATAAATG$"
    #text = "ACA$"
    #text = "ATTCT$"
    result = build_suffix_tree(text)
    print("\n".join(result))


if __name__ == '__main__':
    main()
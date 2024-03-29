# python3

# Good job! (Max time used: 1.09/10.00, max memory used: 55156736/536870912.) <- global text object
# Good job! (Max time used: 1.15/10.00, max memory used: 36139008/536870912.) <- text object passed as explicit are to functions
# Good job! (Max time used: 1.16/10.00, max memory used: 36966400/536870912.) <- Node has index and prev props
# Good job! (Max time used: 2.25/10.00, max memory used: 55574528/536870912.) <- Added suffix_start_pos to Node 

import sys
print(sys.path)
import queue # for BFS in find_shortest_nonshared

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
    def __init__ (self, node_next, 
        label_start=0, label_length=0, 
        prev=-1, index=-1, 
        suffix_start_pos=-1,
        has_text2=False):

        self.next = node_next # key = first symbol in label, value = index in tree
        self.label = (label_start, label_length) # startIndex, length in original text
        self.prev = prev # the node that lead to this. aka the parent node.
        self.index = index # this node's own index. only storing for printing convenience
        self.suffix_start_pos = suffix_start_pos
        self.has_text2 = has_text2


def add_child(text, tree, parent, 
    label_start, label_length, 
    node_next,
    suffix_start_pos,
    has_text2):

    """Adds a child node to the given suffix tree."""
    len_tree = len(tree)
    prev = parent.index
    child = Node(node_next, label_start, label_length, prev, len_tree, suffix_start_pos, has_text2)

    child_symbol = text[label_start]
    if child_symbol in parent.next:
        print("parent node [{}] already has a child [{}] with symbol {} but still adding child [{}]" \
            .format(parent.index, parent.next[child_symbol], child_symbol, len_tree))
        tree.append(child)
        print_tree(tree, text)
        sys.exit()
    parent.next[child_symbol] = len_tree
    tree.append(child)

    if node_next: # implies we changed parents of some nodes, so update their prev values to newly add child's index
        for child_node_index in node_next.values():
            child_node = tree[child_node_index]
            child_node.prev = len_tree


def add_pattern_to_tree(tree, text, pattern, suffix_start_pos, has_text2):
    """Digests given pattern and adds nodes to given suffix tree."""

    # starting from root node, traverse path, add new node, or split existing node in to two, then return
    #print("adding pattern {}".format(pattern))
    i = suffix_start_pos # we'll use a different var since "i" changes, and we need a reference to orig value
    node = tree[0] # start at root node
    if has_text2:
        pass
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
                # implies the pattern is on the right path, since the node's label completely matched
                # we need to head further down this path
                if has_text2:
                    print("setting node [{}] has_text2 to True".format(node.index))
                node.has_text2 = has_text2 # setting this to new value since this node is being re-visited
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
                node_next = child1_node_next,
                suffix_start_pos = node.suffix_start_pos, 
                has_text2 = has_text2)

            # add second child
            add_child(text, tree, node, 
                label_start = i + length_matched, 
                label_length = len(pattern) - length_matched,
                node_next = {},
                suffix_start_pos = suffix_start_pos, 
                has_text2 = has_text2)

            # update this node's label
            node.label = (start, length_matched)
            node.suffix_start_pos = -1 # removing this node's suffix_start_pos as this is not a leaf anymore

            return
        else:
            # implies we'll add a new child node since none exists with this symbol
            # also update current node's next dictionary, to point to this node, for the current symbol
            add_child(text, tree, node,
                label_start = i,
                label_length = len(pattern),
                node_next = {},
                suffix_start_pos = suffix_start_pos, 
                has_text2 = has_text2)

            node.suffix_start_pos = -1 # removing this node's suffix_start_pos as this is not a leaf anymore
            
            return


def print_tree(tree, text):
    for index, node in enumerate(tree):
        print("{: 3}->{: 3}->{}:{}:{}:{}".format(
            node.prev, index, node.next, 
            node.suffix_start_pos, 
            node.has_text2, 
            text[node.label[0] : node.label[0] + node.label[1]]))


def print_leaves(tree, text):
    for index, node in enumerate(tree):
        if node.suffix_start_pos > -1:
            print("{: 3}->{: 3}->{}:{}:{}".format(
                node.prev, index, node.next, 
                node.suffix_start_pos, 
                text[node.label[0] : node.label[0] + node.label[1]]))


def find_shortest_nonshared(tree, text):
    shortest_nonshared = ""
    shortest_nonshared_len = 0
    # traverses tree till we land on first node where has_text2 is False
    # do BFS
    q = queue.Queue()
    q.put( (0, tree[0]) ) # second value is a node, first value is the index into suffix, to get to this node
    while not q.empty():
        suffix_index, node = q.get()

        #print("adding label from node [{}] to shortest_nonshared".format(node.index))
        #shortest_nonshared += text[node.label[0] : node.label[0] + node.label[1]] # appending incoming edge's text, 
                                                                                  # since this text is shared with text2
        child_node_indices = [i for i in node.next.values()]
        for child_node_index in child_node_indices:
            child_node = tree[child_node_index]
            if child_node.has_text2:
                # this child node too has text that is shared with text2, so add it to queue
                q.put( (suffix_index + child_node.label[1], child_node) )
            elif text[child_node.label[0]] != "#":
                # found a child node that does not have text2, so return string made up so far
                #print("adding label from node [{}] to shortest_nonshared".format(child_node.index))
                #shortest_nonshared += text[child_node.label[0]] # added one symbol from this node 
                                                          # to make this string non-shared with text2
                shortest_nonshared_len = suffix_index + 1

                # to find the actual matching string, we need to traverse up the tree
                shortest_nonshared = text[child_node.label[0]]
                prev_node = tree[child_node.prev]
                while prev_node.prev > -1:
                    shortest_nonshared += text[prev_node.label[0] : prev_node.label[0] + prev_node.label[1]]
                    prev_node = tree[prev_node.prev]
                break
    print("shortest non-shared-len", shortest_nonshared_len)
    return "".join(reversed(shortest_nonshared))

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
    root_node = Node(node_next={}, index=0, has_text2=True)
    suffix_tree.append(root_node)

    #find start of text2
    start_text2 = text.find("#") - 1

    # now adding each suffix pattern to the tree
    for i in range(len(text)):
        pattern = text[i:]
        # now traverse tree, adding new node, or splitting existing node
        if i > start_text2:
            has_text2 = True
        else:
            has_text2 = False
        add_pattern_to_tree(suffix_tree, text, pattern, i, has_text2 = has_text2)

    # using generator comprehension :)
    labels = (node.label for node in suffix_tree)
    #result = (text[start : start + length] for start, length in labels if length)

    #print_leaves(suffix_tree, text)
    #print("\n--------------------------------------------------------\n")
    print_tree(suffix_tree, text)
    print("\n--------------------------------------------------------\n")

    shortest_nonshared_substring = find_shortest_nonshared(suffix_tree, text)
    print("shortest_nonshared_substring = {}".format(shortest_nonshared_substring))

    return result


def main():
    #text = sys.stdin.readline().strip()
    #text = "ATAAATG$"
    #text = "ACA$"
    #text = "ATTCT$"
    text = "ATGCGATGACCTGACTGA#CTCAACGTATTGGCCAGA$"
    result = build_suffix_tree(text)
    print("\n".join(result))


if __name__ == '__main__':
    main()
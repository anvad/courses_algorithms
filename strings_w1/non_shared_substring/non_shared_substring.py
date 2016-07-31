# python3

# Good job! (Max time used: 3.21/8.00, max memory used: 12681216/1073741824.) <-- orig file 
# Good job! (Max time used: 2.22/8.00, max memory used: 12677120/1073741824.) <-- removed a couple if sys.exit if checks
# Good job! (Max time used: 2.26/8.00, max memory used: 12664832/1073741824.) <-- removed one if check in add_child
# Good job! (Max time used: 2.29/8.00, max memory used: 12640256/1073741824.) <-- removed call to add_child
# Good job! (Max time used: 4.78/8.00, max memory used: 12693504/1073741824.) <-- current version! should be similar to 2nd version

import sys
import queue # for BFS in find_shortest_nonshared

# build suffix_tree, marking each node that is needed to represent symbols from the second text
#   during build, also capture previous (i.e. parent node's index), so we can travel back from any node to the root
# then, do weighted BFS to search for (the closest to root) node, whose symbol is not part of second text
# then, using the prev (previous) values, re-construct the non-shared string


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

    # if this new child will become the new parent of node's children, 
    #   update these children's parent index, to point to new child
    if node_next:
        for child_node_index in node_next.values():
            child_node = tree[child_node_index]
            child_node.prev = len_tree


def add_pattern_to_tree(tree, text, pattern, suffix_start_pos, has_text2):
    """Digests given pattern and adds nodes to given suffix tree."""

    # starting from root node, traverse path, add new node, or split existing node in to two, then return
    #print("adding pattern {}".format(pattern))
    i = suffix_start_pos # we'll use a different var since "i" changes, and we need a reference to orig value
    node = tree[0] # start at root node

    while True:
        symbol = pattern[0] # get the first char of pattern
        if symbol in node.next:
            # implies this node has a child whose label starts with symbol, so pursue that path

            node = tree[node.next[symbol]] # immediately move to the matching node
            node_has_text2 = node.has_text2 # saving original value for use in creating first child
            node.has_text2 = has_text2 # setting this to new value since this node is being re-visited
            start, length = node.label

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
                pattern = pattern[length_matched:] # we shorten the pattern to search for, since 
                                                   # part of it's already in the tree
                i += length_matched # and we also need to advance the start index of label we'll attach
                #print("chopped pattern to '{}' on node [{}]".format(pattern, node.index))
                #if not pattern:
                #    print("somehow chopped down pattern to empty string")
                #    print_tree(tree, text)
                #    sys.exit()
                continue

            # if i am here, it implies pattern and current node's incoming edge's label matched partially
            # so, we have to add two children
            # child1 will have label's remaining part (i.e. the part that did not match)
            # child2 will have the pattern's remaining part
            # if current node already had children, then these children will now belong to child1 

            len_tree = len(tree)

            if node.next: # implies this node has children!
                child1_node_next = node.next
                node.next = {} # re-assigning node.next to new empty dictionary

                ## since child1 will become the new parent of node's children, 
                ##   updating these children's parent index, to point to new child
                #for child_node_index in child1_node_next.values():
                #    child_node = tree[child_node_index]
                #    child_node.prev = len_tree
            else:
                child1_node_next = {}            

            # add first child
            add_child(text, tree, node, 
                label_start = start + length_matched, 
                label_length = length - length_matched,
                node_next = child1_node_next,
                suffix_start_pos = node.suffix_start_pos, 
                has_text2 = node_has_text2)

            #parent_index = node.index
            #label_start = start + length_matched
            #tree.append(
            #    Node(node_next = child1_node_next,
            #    label_start = label_start,
            #    label_length = length - length_matched,
            #    prev = parent_index,
            #    index = len_tree,
            #    suffix_start_pos = node.suffix_start_pos,
            #    has_text2 = node_has_text2)
            #)
            #node.next[text[label_start]] = len_tree
            #len_tree += 1

            # add second child
            add_child(text, tree, node, 
                label_start = i + length_matched, 
                label_length = len(pattern) - length_matched,
                node_next = {},
                suffix_start_pos = suffix_start_pos, 
                has_text2 = has_text2)

            #label_start = i + length_matched
            #tree.append(
            #    Node(node_next = {},
            #    label_start = label_start,
            #    label_length = len(pattern) - length_matched,
            #    prev = parent_index,
            #    index = len_tree,
            #    suffix_start_pos = suffix_start_pos,
            #    has_text2 = has_text2)
            #)
            #node.next[text[label_start]] = len_tree

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

            #len_tree = len(tree)
            #tree.append(
            #    Node(node_next = {},
            #    label_start = i,
            #    label_length = len(pattern),
            #    prev = node.index,
            #    index = len_tree,
            #    suffix_start_pos = suffix_start_pos,
            #    has_text2 = has_text2)
            #)
            #node.next[text[i]] = len_tree

            # update this node
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


def find_shortest_nonshared(tree, text, string1_delim):
    shortest_nonshared = ""
    shortest_nonshared_len = 0
    # traverses tree till we land on first node where has_text2 is False
    # do weighted BFS using node's label's length as weight (lower weight preferred) - shortest path first
    pq = queue.PriorityQueue()
    # putting root node into queue, as the first item
    pq.put( (0, 0) ) # second value is a node_index, first value is the index into suffix, to get to this node
    while (pq.qsize() > 0):
        suffix_index, node_index = pq.get()
        node = tree[node_index]
        #print("new loop. Dequeued node [{}] with text '{}' and suffix_index {}".format(node.index, 
        #    (text[node.label[0] : node.label[0] + node.label[1]]),
        #    suffix_index))

        # sorting the child nodes based on their lengths, since we want to visit shorter length children first
        child_node_indices = (i for i in node.next.values())
        for child_node_index in child_node_indices:
            child_node = tree[child_node_index]
            if child_node.has_text2:
                # this child node too has text that is shared with text2, so add it to queue
                # remember that the args to priority queue must implement the comparable protocol
                #   hence, we can't store the Node object, but instead we store the node index
                pq.put( (suffix_index + child_node.label[1], child_node_index) )
                #print("put node [{}] with length {} in queue".format(child_node.index, child_node.label[1]))
            elif text[child_node.label[0]] != string1_delim:
                # found a child node that does not have text2, so return string made up so far
                shortest_nonshared_len = suffix_index + 1
                #print("ready to break on node [{}]".format(child_node.index))

                # to find the actual matching string, we need to traverse up the tree
                shortest_nonshared = [text[child_node.label[0]]]
                prev_node = tree[child_node.prev]
                while prev_node.prev > -1:
                    # remember to append the new label as its own element in the list, rather than explode it (+= explodes)
                    #shortest_nonshared += text[prev_node.label[0] : prev_node.label[0] + prev_node.label[1]]
                    shortest_nonshared.append(text[prev_node.label[0] : prev_node.label[0] + prev_node.label[1]])
                    prev_node = tree[prev_node.prev]
                #print("shortest non-shared-len", shortest_nonshared_len)
                return "".join(reversed(shortest_nonshared))
            #else:
            #    pass
            #    #print("i shouldn't be here! node [{}] label '{}' has hash but has_text2 is false!".format(child_node.index, child_node.has_text2) )
    

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
    #labels = (node.label for node in suffix_tree)
    #result = (text[start : start + length] for start, length in labels if length)

    #print_leaves(suffix_tree, text)
    #print("\n--------------------------------------------------------\n")
    #print_tree(suffix_tree, text)
    #print("\n--------------------------------------------------------\n")

    #shortest_nonshared_substring = find_shortest_nonshared(suffix_tree, text)
    #print("shortest_nonshared_substring = {}".format(shortest_nonshared_substring))

    #return shortest_nonshared_substring
    return suffix_tree


def solve(p, q):
    string1_delim = "#"
    string2_delim = "$"
    text = "".join([p, string1_delim, q, string2_delim])
    suffix_tree = build_suffix_tree(text)
    return find_shortest_nonshared(suffix_tree, text, string1_delim)

def main():
    #text = sys.stdin.readline().strip()
    #text = "ATAAATG$"
    #text = "ACA$"
    #text = "ATTCT$"
    #text = "ATGCGATGACCTGACTGA#CTCAACGTATTGGCCAGA$"
    #text = "CCAAGCTGCTAGAGG#CATGCTGGGCTGGCT$"
    p = sys.stdin.readline ().strip ()
    q = sys.stdin.readline ().strip ()
    ans = solve(p, q)
    sys.stdout.write(ans + '\n')


if __name__ == '__main__':
    main()
#Uses python3

#using Kruskal Good job! (Max time used: 0.17/10.00, max memory used: 10133504/536870912.)
#using prim with array based priority queue Good job! (Max time used: 0.07/10.00, max memory used: 10129408/536870912.)
#prim slightly optimized to avoid find dij in some cases Good job! (Max time used: 0.06/10.00, max memory used: 10133504/536870912.)

import sys
import math
from functools import reduce

def minimum_distance(x, y):
    result = 0.
    #write your code here
    """
    here, we have to consider all possible edges, so E is proportional to V^2
    so, we can use Kruskal or Prim with array based implementation
    """
    result = min_dist_pa(x, y)
    return result

"""
Prim implementation with array
"""
def min_dist_pa(x, y):
    result = 0
    max_dist = 10**4 # given that x or y will be between -10^3 and +10^3, the max dist between any two points will be less than 10^4
    num_vertices = len(x)
    cost = [max_dist for i in range(num_vertices)]
    parent = [None for i in range(num_vertices)]

    # hacky priority queue implementation using array. Here i've initialied a queue with num_vertices elements
    pqa = [(max_dist, i) for i in range(num_vertices)]
    pqa_size = len(pqa)

    s = 0 # i.e. starting with 0th vertex as root
    cost[s] = 0
    pqa[0] = (0, 0)
    #print(pqa)
    while pqa_size > 0:
        (d_min, i) = min(pqa)
        pqa_size = pqa_size - 1 # reducing pqa size by one since we are "extracting a node"
        pqa[i] = (max_dist + 1, i) # setting this element to a value higher than max_dist, as a way to mark this vertex as extracted
        result = result + d_min
        for j in range(num_vertices):
            # making sure we calc edge weights (i.e. dij) with neighbors only, rather than with itself!
            # also making sure to both calculating dij only if j is currently in priority queue
            if (j != i) and (pqa[j][0] <= max_dist): # implies vertex j is in priQ 
                dij = math.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
                if (cost[j] > dij):
                    cost[j] = dij
                    parent[j] = i
                    pqa[j] = (dij, j)
    #return reduce(lambda x,y: x+y, cost)
    return result


"""
Kruskal implementation
"""
def min_dist_k(x, y):
    result = 0
    num_vertices = len(x)
    dj = disjoint_set(num_vertices) # created disjoint set of all vertices
    
    # now creating ordered list of all edges
    dist = []
    for i in range(num_vertices):
        for j in range(num_vertices):
            dij = math.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
            dist.append((dij, i, j))
    dist.sort()

    for (dij, i, j) in dist:
        if dj.find(i) != dj.find(j):
            # it means this edje i, j with dist dij is part of MST, so add dij to MST resultant distance
            dj.union(i, j)
            result = result + dij
    return result

"""
disjoint set implementation make_set, find, union
"""
class disjoint_set:
    def __init__(self, size):
        self.size = size
        self.parent = [i for i in range(self.size)]
        self.rank = [0 for i in range(self.size)]
        self.num_sets = size # initially, number of disjoint sets will be equal to size, since each element is in its own set
    def make_set(self, i): # don't use this, since i am making set during init phase
        self.parent[i] = i
        self.rank[i] = 0
        self.num_sets = self.num_sets + 1
    def find(self, i):
        intermediate_nodes = []
        while(i != self.parent[i]):
            i = self.parent[i]
            intermediate_nodes.append(i)
        # now compress the tree
        for j in intermediate_nodes:
            self.parent[j] = i
        return i
    def union(self, i, j):
        i_id = self.find(i)
        j_id = self.find(j)
        if i_id == j_id: # i and j are already in same set, so do nothing
            return
        self.num_sets = self.num_sets - 1 # i and j are in different sets, so merge them and reduce count of disjoint_sets by 1
        if self.rank[i_id] > self.rank[j_id]:
            self.parent[j_id] = i_id
        else:
            self.parent[i_id] = j_id
            if self.rank[i_id] == self.rank[j_id]:
                self.rank[j_id] = self.rank[j_id] + 1
        return
        

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(minimum_distance(x, y)))

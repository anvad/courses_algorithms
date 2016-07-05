#Uses python3

# Good job! (Max time used: 0.11/10.00, max memory used: 10125312/536870912.)

import sys
import math

"""
i am thinking kruskal algo can be used
we'll first calculate all possible dij and sort them in non-descending order
then, make |V| disjoint sets
while num_sets > k
    union(i, j)
return last dij (i.e. when num_sets == k)
"""
def clustering(x, y, k):
    #write your code here
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

    ij = 0
    while dj.num_sets >= k:
        (dij, i, j) = dist[ij]
        dj.union(i, j)
        ij = ij + 1
    return dij

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
    data = data[1:]
    x = data[0:2 * n:2]
    y = data[1:2 * n:2]
    data = data[2 * n:]
    k = data[0]
    print("{0:.9f}".format(clustering(x, y, k)))

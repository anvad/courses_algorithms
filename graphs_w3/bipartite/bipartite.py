#Uses python3

#Good job! (Max time used: 1.61/10.00, max memory used: 54366208/536870912.)

import sys
import queue

def bipartite(adj):
    #write your code here
    num_vertices = len(adj)
    dist = [num_vertices] * num_vertices 
    group = [None] * num_vertices #just a list of vertices and values = true or false to signify which group that vertex belongs to, i.e. "true" group or "false" group
    unexplored = set([i for i in range(num_vertices)]) #create a set of unexplored vertices, just in case we have disjointed graph
    q = queue.Queue()
    while len(unexplored) > 0:
        s = unexplored.pop()
        q.put(s)
        dist[s] = 0
        group[s] = True
        while not q.empty():
            u = q.get()
            neighbors = adj[u]
            #print("neighbors of ", u, " are ", neighbors)
            neighbor_group = not group[u] #all neighbors of u must belong to opposite group
            for v in neighbors:
                if dist[v] == num_vertices: #for all unexplored vertices, assign a group and enqueue them
                    group[v] = neighbor_group
                    dist[v] = dist[u] + 1
                    q.put(v)
                    unexplored.discard(v)
                else:
                    #it means this neighbor has been previously explored, so check if its group is opposite
                    if group[v] != neighbor_group:
                        return 0
    return 1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(bipartite(adj))

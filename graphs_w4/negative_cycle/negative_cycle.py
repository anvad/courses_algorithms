#Uses python3

#Good job! (Max time used: 2.17/10.00, max memory used: 11444224/536870912.)

import sys


def negative_cycle(adj, cost):
    #write your code here
    max_dist = sys.maxsize
    dist = [max_dist for n in adj]
    prev = [None for n in adj]

    num_vertices = len(adj)
    s = 0 #using 0th vertex as my starting point (this is arbitrary and doesn't matter since i really just want to detect presence of negative_cycle)
    dist[s] = 0
    for i in range(num_vertices): #iterate up to n times where n = num_vertices
        relaxed_in_cycle = False
        for u in range(num_vertices): #go thru all edges and relax them
            neighbors = adj[u]
            num_neihgbors = len(neighbors)
            neighbor_costs = cost[u]
            du = dist[u]
            for j in range(num_neihgbors):
                v = neighbors[j]
                du_w = du + neighbor_costs[j]
                if dist[v] > du_w:
                    dist[v] = du_w
                    relaxed_in_cycle = True
        if not relaxed_in_cycle: #if no edge was relaxed in one iteration thru all edges, no need to continue 
            break
    if relaxed_in_cycle: #if the last iteration (i.e. nth iteration) relaxed some edge, it means there is a negative cycle
        return 1
    return 0


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    print(negative_cycle(adj, cost))

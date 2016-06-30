#Uses python3

#with distance_pq: Good job! (Max time used: 0.30/10.00, max memory used: 44220416/536870912.)
#with distance_ar: Good job! (Max time used: 0.49/10.00, max memory used: 44216320/536870912.)

import sys
import queue

#C:\code\courses\algorithms\graphs_w4\dijkstra>py -3 .\dijkstra.py < tests\3

def distance(adj, cost, s, t):
    return distance_ar(adj, cost, s, t)

def distance_ar(adj, cost, s, t):
    #write your code here
    #print("in distance_ar", adj, cost, s, t)
    #return -1
    max_dist = sys.maxsize
    prev = [None for n in adj]
    dist = [max_dist for n in adj]
    dist[s] = 0
    prev[s] = s
    num_vertices = len(adj)
    ar = [(max_dist, i) for i in range(num_vertices)]
    u = s
    num_cycles = 0
    while (u != t) and (num_cycles < num_vertices):
        neighbors = adj[u]
        neighbor_costs = cost[u]
        num_neighbors = len(neighbors)
        for i in range(num_neighbors):
            v = neighbors[i]
            w = neighbor_costs[i]
            if dist[v] > (dist[u] + w):
                dist[v] = dist[u] + w
                prev[v] = u
                ar[v] = (dist[v], v)
                #print("dist_v, v", dist[v], v)
        du,u = min(ar)
        ar[u] = (max_dist, u) #our way of removing this element from consideration
        num_cycles = num_cycles + 1
    if t == s:
        return 0
    if prev[t] == None:
        return -1
    return dist[t]

def distance_pq(adj, cost, s, t):
    #write your code here
    #print("in distance", adj, cost, s, t)
    #return -1
    max_dist = sys.maxsize
    prev = [None for n in adj]
    dist = [max_dist for n in adj]
    dist[s] = 0
    prev[s] = s
    pq = queue.PriorityQueue()
    pq.put((dist[s], s))
    while (pq.qsize() > 0):
        du,u = pq.get()
        if u == t:
            break #break out since the vertex 'u' is in known region and is equal to final vertex 't'
        neighbors = adj[u]
        neighbor_costs = cost[u]
        num_neighbors = len(neighbors)
        for i in range(num_neighbors):
            v = neighbors[i]
            w = neighbor_costs[i]
            if dist[v] > (dist[u] + w):
                dist[v] = dist[u] + w
                prev[v] = u
                pq.put((dist[v], v))
                #print("dist_v, v", dist[v], v)
    if prev[t] == None:
        return -1
    return dist[t]


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
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))

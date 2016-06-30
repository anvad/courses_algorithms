#Uses python3

#Good job! (Max time used: 2.44/10.00, max memory used: 13082624/536870912.)

import sys
import queue


"""
to solve that problem you will need to implement a criterion to determine whether the shortest path from one node to another node in the graph can be made arbitrarily short. The correct criterion for testing that there exist arbitrarily short paths from node S to node u (or, equivalently, that the shortest path from S to u is −∞; or that infinite arbitrage is possible for exchanging US dollars into Russian rubles) is the following:

    Run Bellman-Ford's algorithm to find shortest paths from node S for exactly |V| iterations, where |V| is the number of nodes in the graph.
    Save all the nodes for which the distance estimate was decreased on the V-th iteration - denote the set of these nodes by A.
    Find all nodes reachable from any node in A, use breadth-first search to do that (put all the nodes from A in the queue initially, then run the regular breadth-first search with that queue). Denote the set of these nodes by B.
    There exist arbitrarily short paths from S to u if and only if u is in the set B.
"""
def shortet_paths(adj, cost, s, distance, reachable, shortest):
    #write your code here
    max_dist = distance[0]
    num_vertices = len(adj)
    #distance = [max_dist] * num_vertices

    #first establishing reachability
    bfs_reachable(adj, s, reachable) #this updates the 'reachable' data structure

    distance[s] = 0
    for i in range(num_vertices - 1): #iterate up to n-1 times where n = num_vertices
        relaxed_in_cycle = relax_edges(adj, cost, distance, reachable)
        if not relaxed_in_cycle:
            break
    if relaxed_in_cycle: #it means we need to check at least once more to confirm whether we have negative cycles
        neg_cycle_vertices = set()
        relaxed_in_cycle = relax_edges2(adj, cost, distance, reachable, neg_cycle_vertices)
        if len(neg_cycle_vertices) > 0: #do BFS from each vertex in neg_cycle_vertices set
            bfs(adj, neg_cycle_vertices, shortest)
    #for v in range(num_vertices):
    #    if distance[v] < max_dist:
    #        reachable[v] = 1
    return 0

def bfs_reachable(adj, s, reachable):
    num_vertices = len(adj)
    dist = [num_vertices] * num_vertices 
    q = queue.Queue()
    q.put(s)
    reachable[s] = 1 #setting the starting point as reachable!
    dist[s] = 0 #this is not really the distance, but in this function, all we care about, is to check whether the vertex has been visited (i.e. reachable)
    while not q.empty():
        u = q.get()
        neighbors = adj[u]
        #print("neighbors of ", u, " are ", neighbors)
        for v in neighbors:
            if dist[v] == num_vertices:
                dist[v] = dist[u] + 1
                reachable[v] = 1 #setting this vertex as reachable from s
                q.put(v)
    return
    
def bfs(adj, set_vertices, shortest):
    #print("in bfs", s, t)
    num_vertices = len(adj)
    dist = [num_vertices] * num_vertices 
    q = queue.Queue()
    for v in set_vertices:
        q.put(v)
        shortest[v] = 0 #setting shortest value to 0 for all vertices reachable from s
        dist[v] = 0 #this is not really the distance, but in this function, all we care about, is to check whether the vertex has been visited (i.e. reachable)
    while not q.empty():
        u = q.get()
        neighbors = adj[u]
        #print("neighbors of ", u, " are ", neighbors)
        for v in neighbors:
            if dist[v] == num_vertices:
                dist[v] = dist[u] + 1
                shortest[v] = 0 #setting shortest value to 0 for all vertices reachable from s
                q.put(v)
    return

def relax_edges(adj, cost, dist, reachable):
    num_vertices = len(adj)
    relaxed_in_cycle = False
    for u in range(num_vertices): #go thru all edges and relax them
        if reachable[u] == 0:
            continue #no need to check neighbors of this node since this node is not reachable
        du = dist[u]
        neighbors = adj[u]
        num_neighbors = len(neighbors)
        neighbor_costs = cost[u]
        for j in range(num_neighbors):
            v = neighbors[j]
            du_w = du + neighbor_costs[j]
            if dist[v] > du_w:
                dist[v] = du_w
                relaxed_in_cycle = True
    return relaxed_in_cycle

def relax_edges2(adj, cost, dist, max_dist, neg_cycle_vertices):
    num_vertices = len(adj)
    relaxed_in_cycle = False
    for u in range(num_vertices): #go thru all edges and relax them
        if reachable[u] == 0:
            continue #no need to check neighbors of this node since this node is not reachable
        du = dist[u]
        neighbors = adj[u]
        num_neighbors = len(neighbors)
        neighbor_costs = cost[u]
        for j in range(num_neighbors):
            v = neighbors[j]
            du_w = du + neighbor_costs[j]
            if dist[v] > du_w:
                dist[v] = du_w
                relaxed_in_cycle = True
                neg_cycle_vertices.add(v)
    return relaxed_in_cycle

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
    s = data[0]
    s -= 1
    distance = [10**19] * n
    reachable = [0] * n
    shortest = [1] * n
    shortet_paths(adj, cost, s, distance, reachable, shortest)
    for x in range(n):
        if reachable[x] == 0:
            print('*')
        elif shortest[x] == 0:
            print('-')
        else:
            print(distance[x])


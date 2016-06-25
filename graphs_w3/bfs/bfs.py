#Uses python3

#Good job! (Max time used: 1.65/10.00, max memory used: 46682112/536870912.)

import sys
import queue

def distance(adj, s, t):
    #write your code here
    (dist,prev) = bfs(adj, s, t)
    if dist[t] >= len(adj):
        return -1
    else:
        #reconstruct_path(s, t, prev)
        return dist[t]

def reconstruct_path(s,t,prev):
    #print("in reconstruct_path", s, t, prev)
    result = [t]
    v = t
    while v != None:
        v = prev[v]
        result.append(v)
    result.pop() #removes the final element "None" from the list
    if result[-1] == s:
        result.reverse()
        print([v+1 for v in result])
    else:
        print("no path from ", t, " to ", s)
        result = []
    return result
#returns prev (list of nodes leading back to starting node)
#we are also passing the terminating node, so we can stop discovery as soon as we discover it. thus we avoid processing other unneccessary nodes.
def bfs(adj, s, t):
    #print("in bfs", s, t)
    num_vertices = len(adj)
    dist = [num_vertices] * num_vertices 
    prev = [None] * num_vertices
    q = queue.Queue()
    q.put(s)
    dist[s] = 0
    while not q.empty():
        u = q.get()
        neighbors = adj[u]
        #print("neighbors of ", u, " are ", neighbors)
        for v in neighbors:
            if dist[v] == num_vertices:
                prev[v] = u
                dist[v] = dist[u] + 1
                q.put(v)
            if v == t:
                return (dist,prev)
    return (dist,prev)

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
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1
    print(distance(adj, s, t))

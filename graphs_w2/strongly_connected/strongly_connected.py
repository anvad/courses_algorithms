#Uses python3

#Good job! (Max time used: 0.11/5.00, max memory used: 12611584/536870912.)

import sys

sys.setrecursionlimit(200000)

def dfs(adj, used, order, x):
    #write your code here
    used[x] = 1 #marking this vertex as removed from graph, before the for loop since this graph may have cycles!
    neighbors = adj[x]
    for v in neighbors:
        if used[v] == 0:
            dfs(adj, used, order, v)
    order.append(x) #add this node
    return

def toposort(adj):
    used = [0] * len(adj)
    order = []
    #write your code here
    for u in range(len(adj)):
        if used[u] == 0:
            dfs(adj, used, order, u)
    order.reverse()
    return order

def reverse_graph(adj):
    adj_r = [[] for _ in range(len(adj))]
    for v in range(len(adj)):
        neighbors = adj[v]
        for n in neighbors:
            adj_r[n].append(v)
    return adj_r

def dfs2(adj, visited, SCC, x):
    #write your code here
    visited[x] = 1
    SCC.add(x)
    neighbors = adj[x]
    for v in neighbors:
        if visited[v] == 0:
            dfs2(adj, visited, SCC, v)
    return

def number_of_strongly_connected_components(adj):
    result = 0
    #write your code here
    #create G_r (reversed grapgh) adj_r and find list of vertices sorted by reverse post order 
    adj_r = reverse_graph(adj)
    ordered_vertices = toposort(adj_r)
    #print("ordered_vertices: ", ordered_vertices)
    SCCs = [] #list of lists, each inner list contains the vertices that belong to a strongly connected component
    visited = [0] * len(adj)
    for v in ordered_vertices:
        if visited[v] == 0:
            SCC = set()
            dfs2(adj, visited, SCC, v)
            SCCs.append(SCC)
    result = len(SCCs)
    #for SCC in SCCs:
    #    print("SCC: ", SCC)
    return result

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(number_of_strongly_connected_components(adj))

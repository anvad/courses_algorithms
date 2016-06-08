#Uses python3


#Good job! (Max time used: 0.05/5.00, max memory used: 9105408/536870912.)
#Good job! (Max time used: 0.04/5.00, max memory used: 9105408/536870912.)


import sys

def reach(adj, x, y):
    #write your code here
    #we want to start exploring at x, and if we've reached y, then exit true, else if we reach end, exit false
    visited = set();
    reachable = dfs(adj, x, y, visited)
    return reachable

def dfs(adj, u, y, visited):
    visited.add(u);
    neighbors = adj[u]
    if y in neighbors:
        #it means final vertex is reachable!
        return 1
    for v in neighbors:
        if v not in visited:
            reachable = dfs(adj, v, y, visited)
            if reachable == 1:
                return 1
    #i've reached the end of all my descendant vertices and we could not reach y, so return 0
    return 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    x, y = data[2 * m:]
    adj = [[] for _ in range(n)]
    x, y = x - 1, y - 1
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(reach(adj, x, y))

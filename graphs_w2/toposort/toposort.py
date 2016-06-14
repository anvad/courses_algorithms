#Uses python3

#Good job! (Max time used: 1.03/10.00, max memory used: 39170048/536870912.)

import sys

def dfs(adj, used, order, x):
    #write your code here
    neighbors = adj[x]
    for v in neighbors:
        if used[v] == 0:
            dfs(adj, used, order, v)
    postVisit(used, order, x)
    return

def postVisit(used, order, x):
    order.append(x) #add this node
    used[x] = 1 #marking this vertex as removed from graph

def toposort(adj):
    used = [0] * len(adj)
    order = []
    #write your code here
    for u in range(len(adj)):
        if used[u] == 0:
            dfs(adj, used, order, u)
    order.reverse()
    return order

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj)
    for x in order:
        print(x + 1, end=' ')


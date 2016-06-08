#Uses python3


#Good job! (Max time used: 0.05/5.00, max memory used: 9175040/536870912.)


import sys


def number_of_components(adj):
    result = 0
    #write your code here
    not_yet_visited = set([v for v in range(len(adj))])
    components = [] #we'll store each visited set here
    
    while len(not_yet_visited) > 0:
        visited = set()
        u = not_yet_visited.pop()
        explore(adj, u, visited, not_yet_visited)
        components.append(visited)
    return len(components)

def explore(adj, u, visited, not_yet_visited):
    visited.add(u)
    not_yet_visited.discard(u)
    neighbors = adj[u]
    for v in neighbors:
        if v not in visited:
            explore(adj, v, visited, not_yet_visited)
    return

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
    print(number_of_components(adj))

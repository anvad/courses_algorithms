#Uses python3

#Good job! (Max time used: 0.07/5.00, max memory used: 8753152/536870912.)

import sys


def acyclic(adj):
    not_yet_visited = set([v for v in range(len(adj))]) #contains all vertices that have not yet been visited
    
    result = 0
    ancestors = set()
    while len(not_yet_visited) > 0:
        u = not_yet_visited.pop()
        ancestors.add(u)
        result = explore(adj, u, ancestors, not_yet_visited)
        if result == 1:
            return 1
        ancestors.discard(u)
    return result

def explore(adj, u, ancestors, not_yet_visited):
    ancestors.add(u) #add this node to the ancestors chain before exploring neighbors
    not_yet_visited.discard(u) #if this vertex is present in a cycle, we'll discover it before we leave this function call, hence we don't have to visit this vertex again
    neighbors = adj[u]
    result = 0

    #before we even explore the neighbors, we can check whether any of my current neighbors are also my ancestors
    reachable_ancestors = list(filter( (lambda x: x in ancestors), neighbors  ))
    if len(reachable_ancestors) > 0:
        result = 1
        #for v in neighbors:
        #    print("edge: ", u+1, v+1)
    else:
        #it means none of my immediate neighbors are my ancestors, so let's explore my neighbors
        for v in neighbors:
            result = explore(adj, v, ancestors, not_yet_visited)
            if result == 1: #we've found a cycle
                #print("------")
                #print("edge: ", u+1, v+1)
                break
    ancestors.discard(u) #remove vertex from ancestors chain before return to this vertex' immediate ancestor, as we are done exploring all descendants of this vertex
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
    print(acyclic(adj))

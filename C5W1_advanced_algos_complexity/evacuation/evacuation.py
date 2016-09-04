# python3

import sys
import queue
import datetime

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to_, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to_, capacity)
        backward_edge = Edge(to_, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to_].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id_):
        return self.edges[id_]

    def add_flow(self, id_, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id_].flow += flow
        self.edges[id_ ^ 1].flow -= flow
        e = self.edges[id_]
        #print("adding flow '{}' from node '{}' to '{}'. Remaining capacity = {}".format(
        #    flow, e.u + 1, e.v + 1, e.capacity - e.flow))


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def bfs(graph, S, T):
    """finds shortest viable path from node_0 to node_n
       given a graph, finds the path with least number of viable edges, from S to T
       only edges that are not saturated are considered viable
    """
    #print("S={}, T={}".format(S, T))
    max_possible_flow = 2 * 10 ** 8
    q = queue.Queue()
    q.put( (S,[],[0],max_possible_flow) )
    visited_edges = set()
    while not q.empty():
        node_id, edges_in_path, nodes_in_path, max_flow_in_path_orig = q.get()
        #find all neighbors of this node, and add those neighbors to the queue that have available capacity
        neighboring_edge_ids = graph.get_ids(node_id) # finds all outgoing edges
        for ne_id in neighboring_edge_ids:
            #if ne_id % 2 > 0:
            #    continue # ignoring backward pointing edges
            if ne_id in visited_edges:
                #print("edge {} already visited".format(ne_id))
                continue
            visited_edges.add(ne_id)
            ne = graph.get_edge(ne_id)
            if ne.u == ne.v:
                continue # ignore edges looping back to same node!
            #if ne.v in nodes_in_path:
            #    #print("node {} already visited".format(ne.v))
            #    continue
            #visited_nodes.add(ne.v)
            avail_capacity = ne.capacity - ne.flow
            if avail_capacity > 0:
                new_edges_in_path = edges_in_path.copy()
                new_edges_in_path.append(ne_id)
                max_flow_in_path = max_flow_in_path_orig
                if avail_capacity < max_flow_in_path_orig:
                    #print("avail_capacity '{}' between nodes {} and {} is lower than current path capacity {}".format(
                    #    avail_capacity, ne.u+1, ne.v+1, max_flow_in_path_orig
                    #))
                    max_flow_in_path = avail_capacity
                #new_nodes_in_path = nodes_in_path.copy()
                #new_nodes_in_path.append(ne.v)
                #q.put( (ne.v, new_edges_in_path, new_nodes_in_path, max_flow_in_path) )
                q.put( (ne.v, new_edges_in_path, nodes_in_path, max_flow_in_path) )
                #print("path so far", new_nodes_in_path)
                if ne.v == T:
                    #print("new_nodes_in_path", new_nodes_in_path)
                    return new_edges_in_path, max_flow_in_path

    #print("no viable route found from S to T")
    return [],0


def max_flow(graph, from_, to_):
    flow = 0
    # your code goes here
    while True:
        # find S -> T path using BFS
        edges_in_path,max_flow_in_path = bfs(graph, from_, to_)
        if len(edges_in_path) == 0:
            return flow
        for edge_id in edges_in_path:
            #print("adding flow")
            graph.add_flow(edge_id, max_flow_in_path)

        flow += max_flow_in_path


def main():
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))


if __name__ == '__main__':
    a = datetime.datetime.now()
    main()
    print("time taken: ", datetime.datetime.now() - a)
# python3

# using BFS Good job! (Max time used: 3.82/5.00, max memory used: 15478784/536870912.)
# using DSF Good job! (Max time used: 3.31/5.00, max memory used: 14782464/536870912.)
# using modified Queue in BFS Good job!
#                     (Max time used: 0.89/5.00, max memory used: 15273984/536870912.)
# latest DFS Good job! (Max time used: 1.70/5.00, max memory used: 14786560/536870912.)
# latest BFS Good job! (Max time used: 2.04/5.00, max memory used: 15486976/536870912.)



import queue
import datetime

prev_time = datetime.datetime.now()

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

    def add_fwd_edge(self, from_, to_, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to_, capacity)
        #backward_edge = Edge(to_, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        #self.graph[to_].append(len(self.edges))
        #self.edges.append(backward_edge)

    def add_rev_edges(self):
        num_edges = len(self.edges)
        for id_ in range(num_edges):
            edge = self.edges[id_]
            backward_edge = Edge(edge.v, edge.u, 0)
            self.graph[edge.v].append(len(self.edges))
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
        #e = self.edges[id_]
        #print("adding flow '{}' from node '{}' to '{}'. Remaining capacity = {}".format(
        #    flow, e.u + 1, e.v + 1, e.capacity - e.flow))
    
    def print_edges(self):
        for edge in self.edges:
            #if edge.capacity:
            print("{} ----{}/{}---> {}".format(edge.u, edge.flow, edge.capacity, edge.v))

    def print_edges_by_node(self):
        for node_id in range(self.size()):
            edge_ids = self.get_ids(node_id)
            for edge_id in edge_ids:
                edge = self.get_edge(edge_id)
                print("{} ----{}/{}---> {}".format(edge.u, edge.flow, edge.capacity, edge.v))

def dfs(graph, S, T, qsize):
    """DFS to get from node S to node T, given a graph. Made specifically for bipartite graph"""
    max_flow_in_path = 1 # since this bipartite graph, all edges have capacity 1
    stack = [] # DFS... so using stack
    parent_edges = [-1] * len(graph.edges)
    incoming_edge = -1
    stack.append( (S, incoming_edge) )
    visited_edges = set()
    #num_pops = 0 # a way to track depth of path
    while len(stack):
        node_id, incoming_edge = stack.pop()
        #num_pops += 1

        neighboring_edge_ids = graph.get_ids(node_id) # finds all outgoing edges
        for ne_id in neighboring_edge_ids:
            if ne_id in visited_edges:
                #print("edge {} already visited".format(ne_id))
                continue
            visited_edges.add(ne_id)

            ne = graph.get_edge(ne_id)
            avail_capacity = ne.capacity - ne.flow
            if avail_capacity > 0:
                parent_edges[ne_id] = incoming_edge
                if ne.v == T:
                    #print("num_pops", num_pops)
                    return parent_edges, ne_id, max_flow_in_path

                stack.append( (ne.v, ne_id) )

    return parent_edges, -1, 0


def bfs_builtin_queue(graph, S, T, qsize):
    """finds shortest viable path from node_0 to node_n
       given a graph, finds the path with least number of viable edges, from S to T
       only edges that are not saturated are considered viable
    """
    #print("S={}, T={}".format(S, T))
    max_possible_flow = 1 #2 * 10 ** 8
    #q = queue.Queue(maxsize=qsize)
    q = queue.Queue()
    #q = [None] * qsize
    #q_enq_pointer = 0
    #q_deq_pointer = 0
    parent_edges = [-1] * len(graph.edges)
    incoming_edge = -1
    q.put( (S, incoming_edge, max_possible_flow) )
    #q[q_enq_pointer] = (S, incoming_edge, max_possible_flow)
    #q_enq_pointer += 1
    visited_edges = set()

    #num_checks = 0
    while not q.empty():
    #while q_enq_pointer > q_deq_pointer:
        node_id, incoming_edge, max_flow_in_path = q.get()
        #node_id, incoming_edge, max_flow_in_path = q[q_deq_pointer]
        #q_deq_pointer += 1
        #num_dequeues += 1
        #print("looking at node", node_id)

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
            #if ne.u == ne.v:
            #    continue # ignore edges looping back to same node!

            avail_capacity = ne.capacity - ne.flow
            #num_checks += 1
            if avail_capacity > 0:
            #if ne.flow == 0:
                parent_edges[ne_id] = incoming_edge
                outgoing_node = ne.v
                #new_max_flow_in_path = min(avail_capacity, max_flow_in_path)
                #new_max_flow_in_path = max_flow_in_path
                #if avail_capacity < max_flow_in_path:
                #    #print("avail_capacity '{}' between nodes {} and {} is lower than current path capacity {}".format(
                #    #    avail_capacity, ne.u+1, ne.v+1, max_flow_in_path
                #    #))
                #    new_max_flow_in_path = avail_capacity
                if outgoing_node == T:
                    #return parent_edges, ne_id, new_max_flow_in_path
                    #print("num_dequeues = {}, num_enqueues = {}, num_checks = {}".format(
                    #    q_deq_pointer, q_enq_pointer, num_checks))
                    return parent_edges, ne_id, max_flow_in_path

                #q.put( (ne.v, ne_id, new_max_flow_in_path) )
                q.put( (outgoing_node, ne_id, max_flow_in_path) )
                #q[q_enq_pointer] = (outgoing_node, ne_id, max_flow_in_path)
                #q_enq_pointer += 1
                #num_enqueues += 1
                

    #print("no viable route found from S to T")
    return parent_edges, -1, 0


def bfs(graph, S, T, qsize):
    """finds shortest viable path from node_0 to node_n
       given a graph, finds the path with least number of viable edges, from S to T
       only edges that are not saturated are considered viable
    """
    #print("S={}, T={}".format(S, T))
    max_possible_flow = 1 #2 * 10 ** 8

    q = [None] * qsize
    q_enq_pointer = 0
    q_deq_pointer = 0
    
    parent_edges = [-1] * len(graph.edges)
    incoming_edge = -1
    
    q[q_enq_pointer] = (S, incoming_edge, max_possible_flow)
    q_enq_pointer += 1
    
    visited_edges = set()

    #num_checks = 0
    while q_enq_pointer > q_deq_pointer:
        node_id, incoming_edge, max_flow_in_path = q[q_deq_pointer]
        q_deq_pointer += 1

        #find all neighbors of this node, and add to the queue, those neighbors that have available capacity
        neighboring_edge_ids = graph.get_ids(node_id) # finds all outgoing edges
        for ne_id in neighboring_edge_ids:
            if ne_id in visited_edges:
                #print("edge {} already visited".format(ne_id))
                continue
            visited_edges.add(ne_id)
            ne = graph.get_edge(ne_id)
            #if ne.u == ne.v:
            #    continue # ignore edges looping back to same node!

            avail_capacity = ne.capacity - ne.flow
            #num_checks += 1
            if avail_capacity > 0:
                parent_edges[ne_id] = incoming_edge
                outgoing_node = ne.v
                if outgoing_node == T:
                    #print("num_dequeues = {}, num_enqueues = {}, num_checks = {}".format(
                    #    q_deq_pointer, q_enq_pointer, num_checks))
                    return parent_edges, ne_id, max_flow_in_path

                q[q_enq_pointer] = (outgoing_node, ne_id, max_flow_in_path)
                q_enq_pointer += 1
                

    #print("no viable route found from S to T")
    return parent_edges, -1, 0


def max_flow(graph, from_, to_):
    global prev_time
    flow = 0
    # your code goes here

    #qsize = (graph.size/2) ** 2 + 2 * (graph.size/2) # this is the maximum number of possible edges
    qsize = len(graph.edges)//2

    while True:
        # find S -> T path using BFS
        #print("qsize",qsize)
        parent_edges, last_edge, max_flow_in_path = bfs(graph, from_, to_, qsize)
        #a = datetime.datetime.now()
        #print("{} BFS returned".format(a - prev_time))
        prev_time = a
        if last_edge == -1:
            return flow
        
        # starting with the last_edge, traverse back to first edge
        prev_edge_id = last_edge
        #path_length = 1
        while prev_edge_id != -1:
            #print("adding flow")
            graph.add_flow(prev_edge_id, max_flow_in_path)
            prev_edge_id = parent_edges[prev_edge_id]
            #path_length += 1

        #print("path_length", path_length)
        #a = datetime.datetime.now()
        #print("{} updated flows".format(a - prev_time))
        #prev_time = a

        flow += max_flow_in_path


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, adj_matrix):
        global prev_time
        # Replace this code with an algorithm that finds the maximum
        # matching correctly in all cases.
        n = len(adj_matrix)
        m = len(adj_matrix[0])
        matching = [-1] * n
        # convert the adj_matrix into a flowgraph, so we can run the max_flow algo
        vertex_count = 1 + n + m + 1 # includes inserted S and T vertices
        S = 0
        T = m + n + 1
        graph = FlowGraph(vertex_count)
        for j in range(0, m, 1):
            graph.add_edge(n+j+1, T, 1) # adding edges from vertices in right column to T
            #graph.add_fwd_edge(n+j+1, T, 1) # adding edges from vertices in right column to T

        for i in range(0, n, 1):
            for j in range(0, m, 1):
                if adj_matrix[i][j]:
                    graph.add_edge(i+1, n+j+1, 1) # adding edges from left column to right column
                    #graph.add_fwd_edge(i+1, n+j+1, 1) # adding edges from left column to right column

        for i in range(0, n, 1):
            graph.add_edge(0, i+1, 1) # adding edges from S to vertices in left column of bipartite graph
            #graph.add_fwd_edge(0, i+1, 1) # adding edges from S to vertices in left column of bipartite graph
        
        # now adding the reverse edges
        #graph.add_rev_edges()

        #graph.print_edges()
        #print("-----------------------------------------------------------------")
        #graph.print_edges_by_node()
        #a = datetime.datetime.now()
        #print("{} created graph".format(a - prev_time))
        #prev_time = a

        # now find max flow
        num_matches = max_flow(graph, S, T)
        #print("{} num_matches={}".format(datetime.datetime.now(), num_matches))
        #graph.print_edges()

        # now to find all edges with flow = 1 going from vertex in left column to a vertex in right column
        # so, ignore first 2*n edges and last 2*m edges and also every odd edge as that is backward pointing
        #first_edge = 2 * n
        #last_edge = len(graph.edges) - (2 * m)
        first_edge = 2 * m
        last_edge = len(graph.edges) - (2 * n)
        for edge_id in range(first_edge, last_edge, 2):
            edge = graph.edges[edge_id]
            if edge.flow == 1:
                matching[edge.u - 1] = edge.v - n - 1
        return matching

    def solve(self):
        adj_matrix = self.read_data()
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)


def main():
    max_matching = MaxMatching()
    max_matching.solve()


if __name__ == '__main__':
    #global prev_time
    a = datetime.datetime.now()
    #print("{} started".format(a - prev_time))
    #prev_time = a
    main()
    #print("{} finished".format(datetime.datetime.now()))
    #print("time taken: ", datetime.datetime.now() - a)

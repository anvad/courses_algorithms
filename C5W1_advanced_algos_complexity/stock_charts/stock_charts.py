# python3

from pprint import pprint as pp

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

def dfs(graph, S, T):
    """DFS to get from node S to node T, given a graph. Made specifically for bipartite graph"""
    max_flow_in_path = 1 # since this bipartite graph, all edges have capacity 1
    stack = [] # DFS... so using stack
    parent_edges = [-1] * len(graph.edges)
    incoming_edge = -1
    stack.append( (S, incoming_edge) )
    visited_edges = set()
    while len(stack):
        node_id, incoming_edge = stack.pop()

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
                    return parent_edges, ne_id, max_flow_in_path

                stack.append( (ne.v, ne_id) )

    return parent_edges, -1, 0


def max_flow(graph, from_, to_):
    global prev_time
    flow = 0
    # your code goes here
    while True:
        # find S -> T path using BFS
        parent_edges, last_edge, max_flow_in_path = dfs(graph, from_, to_)
        #a = datetime.datetime.now()
        #print("{} BFS returned".format(a - prev_time))
        #prev_time = a
        if last_edge == -1:
            return flow
        
        # starting with the last_edge, traverse back to first edge
        prev_edge_id = last_edge
        while prev_edge_id != -1:
            #print("adding flow")
            graph.add_flow(prev_edge_id, max_flow_in_path)
            prev_edge_id = parent_edges[prev_edge_id]

        #a = datetime.datetime.now()
        #print("{} updated flows".format(a - prev_time))
        #prev_time = a

        flow += max_flow_in_path


class StockCharts:
    def read_data(self):
        n, k = map(int, input().split())
        stock_data = [list(map(int, input().split())) for i in range(n)]
        return stock_data

    def write_response(self, result):
        print(result)

    def update_pairwise_compatible(self, pairwise_compatible, stock_data, stock_a, stock_b):
        stock_a_data = stock_data[stock_a]
        stock_b_data = stock_data[stock_b]
        res = ( i - j for i,j in zip(stock_a_data, stock_b_data) )
        initial_sign = 1
        if stock_a_data[0] < stock_b_data[0]:
            initial_sign = -1
        for data_point in res:
            if data_point * initial_sign > 0:
                continue
            return # if i am at this line, implies we either encountered a 0 data_point, or there was a sign flip, so nothing to update

        # if i am out of the for loop, implies we went through the entire sequence of stock data points for both stocks
        # and there was no overlap or cross-over so, these two stocks are compatible
        pairwise_compatible[stock_a].add(stock_b)
        pairwise_compatible[stock_b].add(stock_a)

    def min_charts(self, stock_data):
        # Replace this incorrect greedy algorithm with an
        # algorithm that correctly finds the minimum number
        # of charts on which we can put all the stock data
        # without intersections of graphs on one chart.
        n = len(stock_data)
        k = len(stock_data[0])
        charts = []

        # for each stock, let's make a set of stocks it is pair-wise compatible with
        pairwise_compatible = [set() for _ in range(n)]
        for stock_a in range(n):
            for stock_b in range(n):
                if stock_a == stock_b:
                    continue # obviously, a stock is not compatible with itself as every point in the chart will overlap!
                if stock_b in pairwise_compatible[stock_a]:
                    continue # nothing to do as these stocks are already compatible
                self.update_pairwise_compatible(pairwise_compatible, stock_data, stock_a, stock_b)

        # now let's create a S stock and a T stock and create edges to create a flow graph
        # bi-partite graph has n stocks in left column with IDs going from 0 to n-1
        # and same n stocks in right column with IDs going from n to 2n-1
        S = 2 * n # node_id of the starting node in the bi-partite graph
        T = 2 * n + 1 # node_id of the terminating node in the bi-partite graph
        vertex_count = 2 * n + 2
        graph = FlowGraph(vertex_count)
        for i in range(0, n, 1):
            graph.add_edge(S, i, 1) # adding edges from S to vertices in left column of bipartite graph
            graph.add_edge(n + i, T, 1) # adding edges from vertices in right column of bipartite graph
        # so, later we'll ignore the first 2 * 2n edges as they connect to S or T fwd and backwards
        # now add edges betwen left and right columns
        for stock_a in range(n):
            set_a = pairwise_compatible[stock_a]
            for stock_b in set_a:
                graph.add_edge(stock_a, n + stock_b, 1)
        
        # now find max flow. This is equivalent to finding max_matching
        num_matches = max_flow(graph, S, T)

        # now to find all edges with flow = 1 going from vertex in left column to a vertex in right column
        # so, ignore first 2*2n edges (connect to S and T), as well as every odd numbered edge (as those are backward pointing)
        first_edge = 4 * n
        last_edge = len(graph.edges)
        matching_groups = [] # contains lists of matching edges. initally, pairs of vertices on either end of a mathing edge
        all_stocks = set(range(n))
        matching_stocks = set()
        pp(matching_stocks)
        for edge_id in range(first_edge, last_edge, 2):
            edge = graph.edges[edge_id]
            if edge.flow == 1:
                matching_groups.append(set([edge.u, edge.v - n]))
                matching_stocks.add(edge.u)
                matching_stocks.add(edge.v - n)
                pp(matching_stocks)

        pp("matching_groups")
        pp(matching_groups)
        #now, using disjoint set logic, merge sets
        for i in range(len(matching_groups)):
            set_a = matching_groups[i]
            for j in range(len(matching_groups)):
                set_b = matching_groups[j]
                print("before: set_a={} set_b={}".format(set_a, set_b))
                if set_a is set_b:
                    continue
                if set_a.intersection(set_b):
                    new_points = set_b - set_a
                    set_b.clear()
                    for new_point in new_points:
                        b_compatible = True
                        for point in set_a:
                            if (point != new_point) and (point not in pairwise_compatible[new_point]):
                                # it means new_point is not compatible with set_a, so leave point in set_b
                                set_b.add(new_point)
                                b_compatible = False
                                break
                        if b_compatible:
                            set_a.add(new_point)

                    print("after: set_a={} set_b={}".format(set_a, set_b))

        final_group_num = len([1 for i in matching_groups if len(i) > 0])
        # don't forget to add the remaining un-matched stocks into their own charts!!
        num_remaining_stocks = len(all_stocks - matching_stocks)
        pp(all_stocks)
        pp(matching_stocks)
        pp(matching_groups)

        # now merge these groups using disjoint sets logic
        return final_group_num + num_remaining_stocks

    def min_charts_orig(self, stock_data):
        # Replace this incorrect greedy algorithm with an
        # algorithm that correctly finds the minimum number
        # of charts on which we can put all the stock data
        # without intersections of graphs on one chart.
        n = len(stock_data)
        k = len(stock_data[0])
        charts = []
        for new_stock in stock_data:
            added = False
            for chart in charts:
                fits = True
                for stock in chart:
                    above = all([x > y for x, y in zip(new_stock, stock)])
                    below = all([x < y for x, y in zip(new_stock, stock)])
                    if (not above) and (not below):
                        fits = False
                        break
                if fits:
                    added = True
                    chart.append(new_stock)
                    break
            if not added:
                charts.append([new_stock])
        return len(charts)

    def solve(self):
        stock_data = self.read_data()
        result = self.min_charts(stock_data)
        self.write_response(result)


def main():
    stock_charts = StockCharts()
    stock_charts.solve()


if __name__ == '__main__':
    main()

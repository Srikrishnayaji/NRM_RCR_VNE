from alib.datamodel import Substrate

class SubstrateWrapper(Substrate):
    def __init__(self, name):
        super(SubstrateWrapper, self).__init__(name)
    
    def get_shortest_path_based_on_bandwidth(self, bandwidth):
        edge_set_copy = self.edges.copy()
        self.remove_edges_with_lower_bandwidth(bandwidth, edge_set_copy)
        self.compute_shortest_path()
        self.edges = edge_set_copy

    def compute_shortest_path(self):
        self.shortest_paths_costs = {}
        self.shortest_path = {}
        for u in self.nodes:
            self.shortest_paths_costs[u] = {}
            self.shortest_path[u] = {}
            for v in self.nodes:
                if u is v:
                    self.shortest_paths_costs[u][v] = 0
                    self.shortest_path[u][v] = []
                else:
                    self.shortest_paths_costs[u][v] = None
                    self.shortest_path[u][v] = []
        for (u, v) in self.edges:
            self.shortest_paths_costs[u][v] = self.edge[(u, v)][self._shortest_paths_attribute_identifier]
            self.shortest_path[u][v] = []
        for k in self.nodes:
            for u in self.nodes:
                for v in self.nodes:
                    if self.shortest_paths_costs[u][k] is not None and self.shortest_paths_costs[k][v] is not None:
                        cost_via_k = self.shortest_paths_costs[u][k] + self.shortest_paths_costs[k][v]
                        if self.shortest_paths_costs[u][v] is None or cost_via_k < self.shortest_paths_costs[u][v]:
                            self.shortest_paths_costs[u][v] = cost_via_k
                            if self.shortest_path[u][v] == []:
                                self.shortest_path[u][v] = self.shortest_path[u][k] + [k] + self.shortest_path[k][v]

    def remove_edges_with_lower_bandwidth(self, bandwidth, edge_set_copy):
        for edge in edge_set_copy:
            edge_bandwidth = self.get_edge_capacity(edge)
            if edge_bandwidth < bandwidth:
                self.edges.remove(edge)
    
    def update_bandwidth(self, u, v, bandwidth):
        self.get_shortest_path_based_on_bandwidth(bandwidth)
        nodes_between = self.shortest_path[u][v]
        cost = self.shortest_paths_costs[u][v]
        if cost == None:
            print("No path possible")
        else:
            if nodes_between == []:
                self.edge[(u, v)]['capacity'] -= bandwidth
                self.edge[(v, u)]['capacity'] -= bandwidth
            else:
                for node in nodes_between:
                    self.edge[(u, node)]['capacity'] -= bandwidth
                    self.edge[(node, u)]['capacity'] -= bandwidth
                self.edge[(u, v)]['capacity'] -= bandwidth
                self.edge[(v, u)]['capacity'] -= bandwidth
        
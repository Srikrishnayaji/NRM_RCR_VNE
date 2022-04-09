from collections import OrderedDict, namedtuple


def NRM_value(func):
    def wrapper(graph):
        NRM_value_dict = {}
        for node in graph.get_nodes():
            NRM_value_dict[node] = 0
        func(graph, NRM_value_dict)
        NRM_value_dict = OrderedDict(sorted(NRM_value_dict.items(), key = lambda item: item[1], reverse=True))
        return(NRM_value_dict)
    return(wrapper)

@NRM_value
def compute_NRM_value_for_virtual_nodes(graph, NRM_value_dict):
    edges = graph.get_edges()
    for edge in edges:
        demand = graph.get_node_demand(edge[0])
        NRM_value_dict[edge[0]] = ((demand.cpu_request + demand.memory_request) * 
                                    graph.get_edge_demand(edge))

@NRM_value
def compute_NRM_value_for_substrate_nodes(graph, NRM_value_dict):
    edges = graph.get_edges()
    for edge in edges:
        cpu_capacity = graph.get_node_type_capacity(edge[0], "t1")
        memory_capacity = graph.get_node_type_cost(edge[0], "t1")
        NRM_value_dict[edge[0]] += (cpu_capacity + memory_capacity) * graph.get_edge_capacity(edge)


def RCR_value(func):
    def wrapper(graph):
        RCR_value_dict = {}
        nodes = graph.get_nodes()
        for node in nodes:
            func(graph, RCR_value_dict, node)
        return(RCR_value_dict)
    return(wrapper)

@RCR_value
def compute_RCR_value_for_substrate_nodes(graph, RCR_value_dict, node):
    cpu_capacity = graph.get_node_type_capacity(node, "t1")
    memory_capacity = graph.get_node_type_cost(node, "t1")
    RCR_value_dict[node] = (cpu_capacity / memory_capacity)
    return(RCR_value_dict)

@RCR_value
def compute_RCR_value_for_virtual_nodes(graph, RCR_value_dict, node):
    demand = graph.get_node_demand(node)
    RCR_value_dict[node] = (demand.cpu_request / demand.memory_request)
    return(RCR_value_dict)

def get_edgeBandwidth_list(graph):
    bw_edge_tuple = namedtuple("bw_edge_tuple", ["bw", "edge"])
    bw_edge_list = []
    edges = graph.get_edges()
    for edge in edges:
        bandwidth = graph.get_edge_demand(edge)
        bw_edge_list.append(bw_edge_tuple(bandwidth, edge))
    bw_edge_list.sort(reverse=True)
    return(bw_edge_list)

def check_mapping_condition_satisfied(substrate_node, 
    virtual_node, 
    is_substrate_node_mapped,
    is_virtual_node_mapped,
    substrate_graph,
    virtual_graph,
    mapping):
    mapping_occured = False
    if not is_substrate_node_mapped[int(substrate_node)]:
        cpu_capacity = substrate_graph.get_node_capacity(substrate_node)
        mem_capacity = substrate_graph.get_node_cost(substrate_node)
        demand   = virtual_graph.get_node_demand(virtual_node)
        if cpu_capacity >= demand.cpu_request and mem_capacity >= demand.memory_request:
            mapping.map_node(virtual_node, substrate_node)
            is_substrate_node_mapped[int(substrate_node)] = True
            is_virtual_node_mapped[int(virtual_node)] = True
            mapping_occured = True
    return(mapping_occured)

class Summary:
    def __init__(self, name):
        self.name = name
        self.node_utilization = {}
        self.node_available = {}
        self.link_utilization = {}
        self.bandwidth_available = {}
    
    def update_node_summary(self, virtual_graph, substrate_graph, is_mapped, mapping):
        requirements = namedtuple("requirements", ["cpu_request", "memory_request"])
        for virtual_node, substrate_node in mapping.mapping_nodes.items():
            if substrate_node == "NA":
                continue
            else:
                self.node_utilization[substrate_node] = virtual_graph.get_node_demand(virtual_node)
                self.node_available[substrate_node] =  requirements(
                    substrate_graph.get_node_type_capacity(substrate_node, "t1") - self.node_utilization[substrate_node].cpu_request,
                    substrate_graph.get_node_type_cost(substrate_node, "t1") - self.node_utilization[substrate_node].memory_request
                )
        for node in range(len(is_mapped)):
            if not is_mapped[node]:
                self.node_utilization[str(node)] = requirements(0, 0)
                self.node_available[str(node)] = requirements(
                    substrate_graph.get_node_type_capacity(str(node), "t1"),
                    substrate_graph.get_node_type_cost(str(node), "t1")
                )
    
    def get_bandwidth_data(self, substrate_graph):
        edges = substrate_graph.get_edges()
        for edge in edges:
            self.bandwidth_available[edge] = substrate_graph.get_edge_capacity(edge)
    
    def update_edge_resoruce_util_data(self, substrate_graph):
        edges = substrate_graph.get_edges()
        for edge in edges:
            self.link_utilization[edge] = self.bandwidth_available[edge] - substrate_graph.get_edge_capacity(edge)
            self.bandwidth_available[edge] = substrate_graph.get_edge_capacity(edge)
    
    def print_summary(self):
        print("SUMMARY: {}".format(self.name))
        print("-------------")
        for node in self.node_utilization.keys():
            print("SUBSTRATE NODE: {}".format(node))
            print("CPU Utilized: {} | Memory Utilized: {}".format(self.node_utilization[node].cpu_request, self.node_utilization[node].memory_request))
            print("CPU Availabe: {} | Memory Available: {}".format(self.node_available[node].cpu_request, self.node_available[node].memory_request))
        print("----------------------------------------------------------------")
        for edge in self.bandwidth_available.keys():
            print("SUBSTRATE Edge: {}".format(edge))
            print("Bandwidth Availabe: {} | Bandwidth utilized: {}".format(self.bandwidth_available[edge], self.link_utilization[edge]))
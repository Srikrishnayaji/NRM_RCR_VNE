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
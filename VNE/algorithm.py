from mapping_wrapper import Results
from utils import (
    compute_NRM_value_for_substrate_nodes, 
    compute_NRM_value_for_virtual_nodes,
    compute_RCR_value_for_substrate_nodes,
    compute_RCR_value_for_virtual_nodes,
    get_edgeBandwidth_list,
    check_mapping_condition_satisfied)

def NRM_VNE_algorithm(substrate_graph, virtual_graph):
    mapping = Results("NRM_VNE_map", virtual_graph, substrate_graph, True)
    NRM_VNE_node_mapping(substrate_graph, virtual_graph, mapping)
    edge_mapping(substrate_graph, virtual_graph, mapping)
    return(mapping)

def edge_mapping(substrate_graph, virtual_graph, mapping):
    bw_edge_list = get_edgeBandwidth_list(virtual_graph)
    for bw_edge in bw_edge_list:
        u, v = bw_edge.edge
        sub_u = mapping.get_mapping_of_node(u)
        sub_v = mapping.get_mapping_of_node(v)
        if sub_u == "NA" or sub_v == "NA":
            mapping.map_edge(bw_edge.edge, "NA")
        else:
            path_possible = substrate_graph.update_bandwidth(sub_u, sub_v, bw_edge.bw)
            if not path_possible:
                mapping.map_edge(bw_edge.edge, "NA")
            else:
                substrate_path = []
                nodes = substrate_graph.shortest_path[u][v] + [sub_v]
                for node in nodes:
                    substrate_path.append((sub_u, node))
                    sub_u = node
                mapping.map_edge(bw_edge.edge, substrate_path)

def NRM_VNE_node_mapping(substrate_graph, virtual_graph, mapping):
    NRM_value_dict_for_virtual_nodes = compute_NRM_value_for_virtual_nodes(virtual_graph)
    is_virtual_node_mapped = [False] * len(NRM_value_dict_for_virtual_nodes)
    NRM_value_dict_for_substrate_nodes = compute_NRM_value_for_substrate_nodes(substrate_graph)
    is_substrate_node_mapped = [False] * len(NRM_value_dict_for_substrate_nodes)
    for virtual_node, _ in NRM_value_dict_for_virtual_nodes.items():
        if is_virtual_node_mapped[int(virtual_node)]:
            continue
        else:
            for substrate_node, __ in NRM_value_dict_for_substrate_nodes.items():
                mapping_occured = check_mapping_condition_satisfied(
                    substrate_node,
                    virtual_node,
                    is_substrate_node_mapped,
                    is_virtual_node_mapped,
                    substrate_graph,
                    virtual_graph,
                    mapping
                )
                if mapping_occured:
                    break
            if not is_virtual_node_mapped[int(virtual_node)]:
                mapping.map_node(virtual_node, "NA")

def RCR_VNE_algorithm(substrate_graph, virtual_graph):
    mapping = Results("RCR_VNE_map", virtual_graph, substrate_graph, True)
    RCR_VNE_node_mapping(substrate_graph, virtual_graph, mapping)
    edge_mapping(substrate_graph, virtual_graph, mapping)
    return(mapping)

def RCR_VNE_node_mapping(substrate_graph, virtual_graph, mapping):
    NRM_value_dict_for_virtual_nodes = compute_NRM_value_for_virtual_nodes(virtual_graph)
    is_virtual_node_mapped = [False] * len(NRM_value_dict_for_virtual_nodes)
    RCR_value_dict_for_substrate_nodes = compute_RCR_value_for_substrate_nodes(substrate_graph)
    RCR_value_dict_for_virtual_nodes = compute_RCR_value_for_virtual_nodes(virtual_graph)
    is_substrate_node_mapped = [False] * len(RCR_value_dict_for_substrate_nodes)
    for virtual_node, _ in NRM_value_dict_for_virtual_nodes.items():
        if is_virtual_node_mapped[int(virtual_node)]:
            continue
        else:
            difference_list = RCR_value_dict_for_substrate_nodes.items()
            difference_list = [[abs(val-RCR_value_dict_for_virtual_nodes[virtual_node]), node] for node, val in difference_list]
            difference_list.sort(reverse=True)
            for __, substrate_node in difference_list:
                mapping_occured = check_mapping_condition_satisfied(
                    substrate_node,
                    virtual_node,
                    is_substrate_node_mapped,
                    is_virtual_node_mapped,
                    substrate_graph,
                    virtual_graph,
                    mapping
                )
                if mapping_occured:
                    break
            if not is_virtual_node_mapped[int(virtual_node)]:
                mapping.map_node(virtual_node, "NA")

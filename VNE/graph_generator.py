from substrate_wrapper import SubstrateWrapper
from alib.datamodel import LinearRequest
from collections import namedtuple

def generate_substrate_graph():
    substrate_graph = SubstrateWrapper("G_s")
    num_substrate_nodes = int(input("Enter the number of substrate nodes: "))
    count = 0
    while(count < num_substrate_nodes):
        cpu_capacity = float(input("Enter the CPU capacity: "))
        memory_cost  = float(input("Enter the memory cost: "))
        substrate_graph.add_node(str(count), {"t1"}, capacity={"t1": cpu_capacity}, cost={"t1": memory_cost})
        count += 1
    print("------------------------------------------------------------------")
    num_substrate_edges = int(input("Enter the number of substrate edges: "))
    count = 0
    while(count < num_substrate_edges):
        u = input("Enter the first node: ")
        v = input("Enter the second node: ")
        edge_bandwidth = float(input("Enter the edge bandwidth: "))
        substrate_graph.add_edge(str(u), str(v), edge_bandwidth)
        count += 1
    return(substrate_graph)

def generate_virtual_graph():
    virtual_graph = LinearRequest("G_v")
    num_virtual_nodes = int(input("Enter the number of virtual nodes: "))
    count = 0
    while(count < num_virtual_nodes):
        cpu_capacity = float(input("Enter the CPU capacity: "))
        memory_cost  = float(input("Enter the memory cost: "))
        requirement = namedtuple("requirement", ["cpu_request", "memory_request"])
        demand = requirement(cpu_capacity, memory_cost)
        virtual_graph.add_node(str(count), demand, "t1")
        count += 1
    print("------------------------------------------------------------------")
    num_virtual_edges = int(input("Enter the number of virtual edges: "))
    count = 0
    while(count < num_virtual_edges):
        u = input("Enter the first node: ")
        v = input("Enter the second node: ")
        edge_bandwidth = float(input("Enter the edge bandwidth: "))
        virtual_graph.add_edge(str(u), str(v), edge_bandwidth)
        count += 1
    return(virtual_graph)
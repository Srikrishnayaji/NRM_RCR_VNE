from VNE.algorithm import NRM_VNE_algorithm, RCR_VNE_algorithm
from VNE.graph_generator import generate_substrate_graph, generate_virtual_graph
import copy

if __name__ == "__main__":
    substrate_graph = generate_substrate_graph()
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    virtual_graph   = generate_virtual_graph()
    substrate_graph_copy = copy.deepcopy(substrate_graph)
    virtual_graph_copy = copy.deepcopy(virtual_graph)
    print("Executing NRM algorithm!")
    print(NRM_VNE_algorithm(substrate_graph, virtual_graph))
    print("Executing RCR algorithm!")
    print(RCR_VNE_algorithm(substrate_graph_copy, virtual_graph_copy))


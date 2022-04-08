from VNE.algorithm import NRM_VNE_algorithm, RCR_VNE_algorithm
from VNE.graph_generator import generate_substrate_graph, generate_virtual_graph

if __name__ == "__main__":
    substrate_graph = generate_substrate_graph()
    virtual_graph   = generate_virtual_graph()
    print(NRM_VNE_algorithm(substrate_graph, virtual_graph))
    print(RCR_VNE_algorithm(substrate_graph, virtual_graph))

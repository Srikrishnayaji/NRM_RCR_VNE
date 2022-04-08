from alib.solutions import Mapping

class Results(Mapping):
    def __init__(self,  name, request, substrate, is_embedded):
        super(Results, self).__init__(name, request, substrate, is_embedded)
    
    def map_node(self, virtual_node, substrate_node):
        self.mapping_nodes[virtual_node] = substrate_node
    
    def map_edge(self, virtual_edge, substrate_path):
        self.mapping_edges[virtual_edge] = substrate_path
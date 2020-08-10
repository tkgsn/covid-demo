  import my_code.mechanism as mechanism
import numpy as np

def make_mechanism_with_policy_graph_class(mechanism_class):
    
    class MechanismWithPolicyGraph(mechanism_class):
        
        def __init__(self, map_processor, epsilon):
            super().__init__(map_processor, epsilon)
            
        def _compute_sensitivity(self, coords, i, j):
            if self.map_processor.graph_mat[self.states[i],self.states[j]] == 1:
                return [(coords[i] - coords[j]), (coords[j] - coords[i])]
            else:
                return []

        def perturb(self, state):
            coord = self.map_processor.state_to_coord(state)
            perturbed_coord = super().perturb(coord)
            perturbed_state = self._find_nearest_state_in_states(perturbed_coord, self.map_processor.set_of_connected_states[self._state_counter(state)])
            return perturbed_state
            
    return MechanismWithPolicyGraph

PlanarIsotropicMechanismWithPolicyGraph = make_mechanism_with_policy_graph_class(mechanism.PlanarIsotropicMechanism)
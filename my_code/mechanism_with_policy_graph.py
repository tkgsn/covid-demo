import my_code.mechanism as mechanism
import numpy as np

def make_mechanism_with_policy_graph_class(mechanism_class):
    
    class MechanismWithPolicyGraph(mechanism_class):
        
        def __init__(self, map_processor, epsilon):
            super().__init__(map_processor, epsilon)
            
        def _compute_sensitivity(self, state1, state2):
            if self.map_processor.graph_mat[state1,state2] == 1:
                return super()._compute_sensitivity(state1, state2)
            else:
                return []

        def perturb(self, state):
            perturbed_coord = super().perturb(state)
            return self._find_nearest_state(perturbed_coord)
        
        def perturb_for_test(self, state):
            perturbed_coord = super().perturb(state)
            perturbed_state_for_test = self._find_nearest_state_in_states(perturbed_coord, self.map_processor.all_states)
            perturbed_state = self._find_nearest_state(perturbed_coord)
            return perturbed_state, perturbed_state_for_test
        
        def _find_nearest_state(self, coord):
            nearest_coord = [coord[0], coord[1]]
            if coord[0] >= self.map_processor.n_x_lattice:
                nearest_coord[0] = self.map_processor.n_x_lattice
            else:
                nearest_coord[0] = int(round(coord[0]))
                
            if coord[1] >= self.map_processor.n_y_lattice:
                nearest_coord[1] = self.map_processor.n_y_lattice
            else:
                nearest_coord[1] = int(round(coord[1]))
                
            if nearest_coord[0] <= 0:
                nearest_coord[0] = 0
                
            if nearest_coord[1] <= 0:
                nearest_coord[1] = 0
            return self.map_processor.coord_to_state(nearest_coord)
                
        def perturb_to_subgraph(self, state):
            perturbed_coord = super().perturb(state)
            perturbed_state = self._find_nearest_state_in_states(perturbed_coord, self.map_processor.connected_states(state))
            return perturbed_state
            
    return MechanismWithPolicyGraph

PlanarIsotropicMechanismWithPolicyGraph = make_mechanism_with_policy_graph_class(mechanism.PlanarIsotropicMechanism)
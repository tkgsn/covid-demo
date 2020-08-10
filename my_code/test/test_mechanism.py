import unittest
import sys
sys.path.append("../")
sys.path.append("../../")
from mechanism_with_policy_graph import PlanarIsotropicMechanismWithPolicyGraph as PIM
from map_processor import Map

class TestMechanism(unittest.TestCase):
    
    def setUp(self):
        self.map_processor = Map(20, 0, 1, 0, 1, 3)
        self.pim = PIM(self.map_processor, 1)
        self.pim.build_distributions()
        
    def test_perturb_to_subgraph(self):
        test_states = [0,1,2,3,4,5,6,7,8,9]
        perturbed_states = [self.pim.perturb_to_subgraph(state) for state in test_states]
        for test_state, perturbed_state in zip(test_states, perturbed_states):
            self.assertIn(perturbed_state, self.pim.map_processor.connected_states(test_state))
            
    def test_perturb(self):        
        #test_states = self.map_processor.all_states
        test_states = [0,1,2,3,4,5]
        perturbed_states = [self.pim.perturb(state) for state in test_states]
        perturbed_states2 = [self.pim.perturb_for_test(state) for state in test_states]
        for test_state, perturbed_state in zip(test_states, perturbed_states):
            self.assertIn(perturbed_state, self.pim.map_processor.all_states)
        for perturbed_state in perturbed_states2:
            self.assertEqual(perturbed_state[0], perturbed_state[1])
        
            
    
if __name__ == '__main__':
    unittest.main()
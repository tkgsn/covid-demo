import unittest
import sys
sys.path.append("../")
from surveil import surveil

class TestSurveil(unittest.TestCase):
    
    def setUp(self):
        self.states_2_2 = [0,0]
        self.states_3_3 = [0,0,0]
        self.states_3_4 = [1,0,0,0]
        self.states_3_10 = [0,1,2,3,4,0,6,7,8,0]
        self.states_6_10 = [0,1,2,1,4,0,6,7,1,0]
        self.states_10_10 = [0,1,2,1,2,0,2,2,1,0]
        
    def test_surveil(self):
        self.assertEqual(surveil(self.states_2_2),2)
        self.assertEqual(surveil(self.states_3_3),3)
        self.assertEqual(surveil(self.states_3_4),3)
        self.assertEqual(surveil(self.states_3_10),3)
        self.assertEqual(surveil(self.states_10_10),10)
    
if __name__ == '__main__':
    unittest.main()
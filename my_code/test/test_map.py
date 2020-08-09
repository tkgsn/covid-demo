import unittest
import sys
sys.path.append("../")
import map_processor

class TestMap(unittest.TestCase):

    def setUp(self):
        self.x_y_equal_map = map_processor.Map(50, 0, 1, 0, 1)
        self.x_2y_map = map_processor.Map(50, 0, 1, 0, 2)
    
    def tearDown(self):
        pass
    
    def test_find_nearest_coord(self):
        lower_left = self.x_y_equal_map.find_nearest_state([0,0])
        upper_right = self.x_y_equal_map.find_nearest_state([1,1])
        lower_right = self.x_y_equal_map.find_nearest_state([1,0])
        upper_left = self.x_y_equal_map.find_nearest_state([0,1])
        middle_left = self.x_y_equal_map.find_nearest_state([0,0.5])
        middle_right = self.x_y_equal_map.find_nearest_state([1,0.5])
        self.assertEqual(lower_left, 0)
        self.assertEqual(upper_right, 51*51 -1)
        self.assertEqual(lower_right, 51 -1)
        self.assertEqual(upper_left, 51*50)
        self.assertEqual(middle_left, 51*25)
        self.assertEqual(middle_right, 51*26 -1)
    
    def test_convert_state_and_coord(self):
        zero_coord = self.x_y_equal_map.state_to_coord(0)
        middle_left_coord = self.x_y_equal_map.state_to_coord(51*25)
        middle_right_coord = self.x_y_equal_map.state_to_coord(51*25 + 25)
        max_coord = self.x_y_equal_map.state_to_coord(51*51 -1)
        self.assertEqual(zero_coord[0], 0)
        self.assertEqual(zero_coord[1], 0)
        self.assertEqual(max_coord[0], 50)
        self.assertEqual(max_coord[1], 50)
        self.assertEqual(middle_left_coord[0], 0)
        self.assertEqual(middle_left_coord[1], 25)
        self.assertEqual(middle_right_coord[0], 25)
        self.assertEqual(middle_right_coord[1], 25)
        self.assertEqual(self.x_y_equal_map.coord_to_state(zero_coord), 0)
        self.assertEqual(self.x_y_equal_map.coord_to_state(max_coord), 51*51 -1)
        self.assertEqual(self.x_y_equal_map.coord_to_state(middle_left_coord), 51*25)
        self.assertEqual(self.x_y_equal_map.coord_to_state(middle_right_coord), 51*25 + 25)
    
    def test_map_range(self):
        self.assertEqual(self.x_y_equal_map.n_x_lattice, self.x_y_equal_map.n_y_lattice)
        self.assertEqual(2 * self.x_2y_map.n_x_lattice, self.x_2y_map.n_y_lattice)
        self.assertEqual(51 * 51, self.x_y_equal_map.n_state)
        self.assertEqual(51 * 101, self.x_2y_map.n_state)
        
if __name__ == '__main__':
    unittest.main()
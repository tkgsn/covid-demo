import numpy as np

class MapProcessor():
    def __init__(self, n_x_lattice):
        self.n_x_lattice = n_x_lattice
        
    def coord_to_state(self, coord):
        return int(coord[0] + coord[1] * (self.n_x_lattice + 1))

    def state_to_coord(self, state):
        return np.array([state % (self.n_x_lattice + 1), int(state / (self.n_x_lattice + 1))])

    def states_to_coords(self, states):
        return np.array([self.state_to_coord(state) for state in states])

    def coords_to_states(self, coords):
        return np.array([self.coord_to_state(coord) for coord in coords])

            
class Map(MapProcessor):
    
    def __init__(self, n_x_lattice, min_x, max_x, min_y, max_y):
        super().__init__(n_x_lattice)
        self._make_map(min_x, max_x, min_y, max_y)
    
    def _make_map(self, min_x, max_x, min_y, max_y):
        
        self.min_x, self.max_x, self.min_y, self.max_y = min_x, max_x, min_y, max_y

        bottom_length = np.linalg.norm([self.min_x - self.max_x, self.min_y - self.min_y])
        side_length = np.linalg.norm([self.min_x - self.min_x,  self.min_y - self.max_y])
        self.lattice_length = bottom_length / self.n_x_lattice
        self.n_y_lattice = round(side_length / self.lattice_length)
        self.n_state = int((self.n_x_lattice + 1) * (self.n_y_lattice + 1))

        self.all_states = list(range(self.n_state))
        self.all_coords = self.states_to_coords(self.all_states)
        
    def find_nearest_state(self, coord):
        coord = np.array([self.n_x_lattice, self.n_y_lattice]) * (np.array([coord[0], coord[1]]) - np.array([self.min_x, self.min_y])) / (np.array([self.max_x - self.min_x, self.max_y - self.min_y]))
        state = int(self.coord_to_state([round(coord[0]), round(coord[1])]))
        return state
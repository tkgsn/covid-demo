import numpy as np
import math
import networkx as nx

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
        
    def state_to_location(self, state):
        coord = self.state_to_coord(state)
        return [self.min_x + (self.max_x-self.min_x)*coord[0]/self.n_x_lattice, self.min_y + (self.max_y-self.min_y)*coord[1]/self.n_y_lattice]
    
    def find_nearest_states(self, coords):
        return [self._find_nearest_state(coord) for coord in coords]
            
    def make_set_of_connected_states(self, graph_mat):
        G = nx.Graph()
        G.add_nodes_from(self.all_states)

        for i, state in enumerate(self.all_states):
            for state_ in self.all_states[i:]:
                if graph_mat[state, state_] == 1:
                    G.add_edge(state, state_)

        return [list(nodes) for nodes in nx.connected_components(G)]
    
    def _make_map(self, min_x, max_x, min_y, max_y):
        
        self.min_x, self.max_x, self.min_y, self.max_y = min_x, max_x, min_y, max_y

        bottom_length = np.linalg.norm([self.min_x - self.max_x, self.min_y - self.min_y])
        side_length = np.linalg.norm([self.min_x - self.min_x,  self.min_y - self.max_y])
        self.lattice_length = bottom_length / self.n_x_lattice
        self.n_y_lattice = math.ceil(side_length / self.lattice_length)
        self.n_state = int((self.n_x_lattice + 1) * (self.n_y_lattice + 1))

        self.all_states = list(range(self.n_state))
        
    def make_graph(self, n_split):
        self._make_area(n_split)
        return self._update_graph_according_to_area()
        
    def _make_area(self, n_split):
        n_x_lattice_in_area = math.ceil((self.n_x_lattice + 1)/n_split)
        
        n_x_area = math.ceil((self.n_x_lattice + 1) / n_x_lattice_in_area)
        n_y_area = math.ceil((self.n_y_lattice + 1) / n_x_lattice_in_area)
        
        n_area = n_x_area * n_y_area
        
        def state_to_area_state(state):
            coord = self.state_to_coord(state)
            
            area_coord = [math.floor(coord[0]/n_x_lattice_in_area), math.floor(coord[1]/n_x_lattice_in_area)]
            return area_coord[0] + area_coord[1] * n_x_area
        
        self.state_to_area_state = state_to_area_state
            
        areas = [[] for _ in range(n_area)]
        for state in self.all_states:
            area_state = state_to_area_state(state)
            areas[area_state].append(state)
            
        self.areas = areas
        
    def _find_nearest_state(self, coord):
        coord = np.array([self.n_x_lattice, self.n_y_lattice]) * (np.array([coord[0], coord[1]]) - np.array([self.min_x, self.min_y])) / (np.array([self.max_x - self.min_x, self.max_y - self.min_y]))
        state = int(self.coord_to_state([round(coord[0]), round(coord[1])]))
        return state
    
    def cp_n_split(self, n_subgraph_x_nodes):
        return math.ceil(self.n_x_lattice/n_subgraph_x_nodes)
    
    def _update_graph_according_to_area(self):   
        graph_mat = np.zeros((self.n_state, self.n_state))

        for counter, state in enumerate(self.all_states):
            for state_ in self.all_states[counter:]:
                if self._is_same_area(state, state_):
                    graph_mat[state,state_] = 1
                    graph_mat[state_,state] = 1

        return graph_mat

    def _is_same_area(self, state1, state2):
        area1 = self.state_to_area_state(state1)
        area2 = self.state_to_area_state(state2)
        return area1 == area2

    def compute_e_dist_from_state(self, state1, state2):
        return np.linalg.norm(self.state_to_coord(state1) - self.state_to_coord(state2)) * self.lattice_length
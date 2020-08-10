import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import scipy
import math
import copy
import joblib
import os

multiplier = 100
hull_coords = np.array([[i,j] for i in range(-multiplier,multiplier) for j in range(-multiplier,multiplier)])

def sample_point_from_body(vertices, n_sample=1):

    if len(vertices) == 1:
        return [vertices[0]]

    x, y = vertices[:,0], vertices[:,1]

    left = np.min(x)
    right = np.max(x)
    lower = np.min(y)
    upper = np.max(y)

    coef = multiplier / np.max([[right-left], [upper-lower]])

    try:
        hull = scipy.spatial.Delaunay(coef * vertices)
        coords = hull_coords[hull.find_simplex(hull_coords)>=0] / coef
        random_inds = np.random.randint(len(coords), size=n_sample)

        return coords[random_inds]
    except:
        return sample_point_from_boundary(vertices, n_sample=n_sample)
    
def sample_point_from_boundary(vertices, n_sample = 1, total_length=None, segments=None):
    if total_length is None:
        total_length, segments = compute_total_length_of_full(vertices)

    samples = np.zeros((n_sample, 2))

    for i in range(n_sample):

        random_length = np.random.rand() * total_length
        temp_total_length = random_length
        for seg_i, segment in enumerate(segments):
            if temp_total_length - segment < 0:
                break
            temp_total_length = temp_total_length - segment

        if seg_i == len(segments)-1:
            seg_j = 0
        else:
            seg_j = seg_i+1

        left_vertex = vertices[seg_i]
        right_vertex = vertices[seg_j]

        samples[i,:] = left_vertex + (right_vertex - left_vertex) * temp_total_length / segment

    return samples


def compute_total_length_of_full(vertices):

    segments = []
    total_length = 0
    for i in range(len(vertices)):
        if i == len(vertices)-1:
            j = 0
        else:
            j = i+1
        segment = np.linalg.norm(vertices[i] - vertices[j])
        segments.append(segment)
        total_length += segment

    return total_length, segments
    
class Noise_generator():
    
    def __init__(self, epsilon, transformed_vertices, T_i):
        self.transformed_vertices = transformed_vertices
        self.T_i = T_i
        self.epsilon = epsilon
        
    def generate(self):
        sample = sample_point_from_body(self.transformed_vertices)[0]
        noise = np.random.gamma(3, 1/self.epsilon, 1)

        z = noise * np.dot(self.T_i, sample.T)

        return z
    
    
class Mechanism():
    def __init__(self, map_processor, epsilon):
        self.map_processor = map_processor
        self.epsilon = epsilon
    
    def perturb(self, state):
        coord = self.map_processor.state_to_coord(state)
        chosen_noise_generator = self.noise_generators[self._connected_states_number(state)]
        return coord + chosen_noise_generator.generate()
    
    def _connected_states_number(self, state):
        for counter, states in enumerate(self.map_processor.set_of_connected_states):
            if state in states:
                return counter
            
    def _find_nearest_state_in_states(self, coord, states):
        min_distance = float("inf")
        coords = self.map_processor.states_to_coords(states)
        for i, coord_ in enumerate(coords):
            distance = np.linalg.norm(coord - coord_)
            
            if distance < min_distance:
                min_distance = distance
                surrogated_loc = coord
                state = states[i]
        
        return state
    
    def inference(self):
        pass

    def _check_included(self, cell_true_loc):
        return np.any(np.all(cell_true_loc == self.coords, axis=1))
    
    def _make_sensitivities(self, states):
        
        sensitivities = []
        
        for i, state1 in enumerate(states):
            for state2 in states[i:]:
                sensitivities += self._compute_sensitivity(state1, state2)
                
        return np.array(sensitivities)
    
    def _compute_sensitivity(self, state1, state2):
        coord1 = self.map_processor.state_to_coord(state1)
        coord2 = self.map_processor.state_to_coord(state2)
        return [coord1 - coord2, coord2 - coord1]
    
    
class PlanarIsotropicMechanism(Mechanism):
    
    def __init__(self, map_processor, epsilon, iso_trans_sample_size=5000):
        super().__init__(map_processor, epsilon)
        
        self.iso_trans_sample_size = iso_trans_sample_size
        
    def inference(self, prior_dist, cell_z):
        
        pos_dist = np.zeros(len(prior_dist))
        pos_dist[self.state_nos] = 1
        
        if len(self.state_nos) == 1:
            return pos_dist
        
        transformed_z = self._transform(cell_z.reshape(-1,2))[0]
        
        inference_probs = {}
        
        for state_no, transformed_coord in zip(self.state_nos, self.transformed_coords):
            k = self._k_norm((transformed_z - transformed_coord))
            inference_probs[state_no] = np.exp(-self.epsilon * k) * prior_dist[state_no]

        inference_sum = np.sum(list(inference_probs.values()))
        inference_probs = {state_no: prob/inference_sum for state_no, prob in inference_probs.items()}

        for state_no, prob in inference_probs.items():
            pos_dist[state_no] = prob
        
        return pos_dist

    
    def _transform(self, vertices, T,):
        return np.dot(T, vertices.T).T
    
    def _make_k_norm(self, vertices):
        
        def k_norm(vec):
            x,y = vec

            n_vertices = len(vertices)
            if n_vertices == 2:
                ks = (vec / vertices)
                k = ks[0][0]
                if np.isnan(k):
                    k = ks[0][1]
                return abs(k)

            a = 0
            k = 0

            for i in range(n_vertices):
                j = i+1
                if j == n_vertices:
                    j = 0
                v1x, v1y = self.vertices[i][0], self.vertices[i][1]
                v2x, v2y = self.vertices[j][0], self.vertices[j][1]

                b = (v2x-(x/y)*v2y)/((x/y)*(v1y-v2y)-v1x+v2x)
                if b>=0 and b<=1 :
                    a = b/y*(v1y-v2y)+v2y/y
                if a > 0:
                    k = 1/a

            return k
        
        return k_norm
            
        
    
    def _k_norm(self, vec):

        x,y = vec
        
        n_vertices = len(self.transformed_vertices)
        if n_vertices == 2:
            ks = (vec / self.transformed_vertices)
            k = ks[0][0]
            if np.isnan(k):
                k = ks[0][1]
            return abs(k)
        elif n_vertices == 1:
            return 0
        
        a = 0
        k = 0
        
        for i in range(n_vertices):
            j = i+1
            if j == n_vertices:
                j = 0
            v1x, v1y = self.transformed_vertices[i][0], self.transformed_vertices[i][1]
            v2x, v2y = self.transformed_vertices[j][0], self.transformed_vertices[j][1]
            
            b = (v2x-(x/y)*v2y)/((x/y)*(v1y-v2y)-v1x+v2x)
            if b>=0 and b<=1 :
                a = b/y*(v1y-v2y)+v2y/y
            if a > 0:
                k = 1/a

        return k

    def build_distribution(self, true_state):
        states = self.map_processor.connected_states(true_state)
        coords = self.map_processor.states_to_coords(states)
        self.coords = coords
        
        sensitivities = self._make_sensitivities(states)
        vertices = self._make_convex_hull(sensitivities)
        T, T_i = self._compute_isotropic_transformation(vertices)

        transformed_vertices = self._transform(vertices, T)
        
        k_norm_generator = Noise_generator(self.epsilon, transformed_vertices, T_i)
        
        return k_norm_generator

    def build_distributions(self):
        self.noise_generators = []
        for states in self.map_processor.set_of_connected_states:
            self.noise_generators.append(self.build_distribution(states[0]))
        
    
    def sample_point_from_boundary(self, vertices, n_sample = 1, total_length=None, segments=None):
        if total_length is None:
            total_length, segments = self.compute_total_length_of_full(vertices)
            
        samples = np.zeros((n_sample, 2))
            
        for i in range(n_sample):

            random_length = np.random.rand() * total_length
            temp_total_length = random_length
            for seg_i, segment in enumerate(segments):
                if temp_total_length - segment < 0:
                    break
                temp_total_length = temp_total_length - segment

            if seg_i == len(segments)-1:
                seg_j = 0
            else:
                seg_j = seg_i+1

            left_vertex = vertices[seg_i]
            right_vertex = vertices[seg_j]
            
            samples[i,:] = left_vertex + (right_vertex - left_vertex) * temp_total_length / segment
        
        return samples
    

    def _compute_isotropic_transformation(self, vertices):
        
        try:
            
            if np.all(vertices == 0) or len(vertices) == 2:
                raise
                
            samples = sample_point_from_body(vertices, n_sample=self.iso_trans_sample_size)

            T = np.average([np.dot(sample.reshape(2,-1), sample.reshape(2,-1).T) for sample in samples], axis=0)
            T = np.linalg.inv(T)
            T = scipy.linalg.sqrtm(T)
            T_i = np.linalg.inv(T)

        except:
            T = np.array([[1,0],[0,1]])
            T_i = np.array([[1,0],[0,1]])
            
        return T, T_i
        

    def _make_convex_hull(self, vertices):
        
        if len(self.coords) <= 2:
            return vertices
        
        else:
            try:
                self.hull = ConvexHull(vertices)
                self.on_line = False
                return vertices[self.hull.vertices]
            
            except:
                #print("Vertices are on linear (>=3)")
                self.on_line = True
                max_distance = -float("inf")
                for i in range(len(vertices)-1):
                    for j in range(i+1, len(vertices)):
                        distance = np.linalg.norm(vertices[i] - vertices[j])
                        if distance > max_distance:
                            max_distance = distance
                            edges = (i,j)
                return np.array([vertices[edges[0]], vertices[edges[1]]])
            
    def _compute_area_of_sensitivity_hull(self):
        area = 0
        
        n_vertices = len(self.vertices)
        
        if n_vertices == 1:
            return area
        
        if self.on_line or n_vertices == 2:
            return np.linalg.norm(self.vertices[0] - self.vertices[1])
        
        for i in range(n_vertices):
            if i == n_vertices:
                j = 0
            else:
                j = i+1
                
            coord0 = self.vertices[i]
            coord1 = self.vertices[j]
            
            area += (1/2)*np.abs(np.linalg.det(np.array([coord0,coord1])))
        
        return area
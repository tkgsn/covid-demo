from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
import numpy as np
import matplotlib.pyplot as plt
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
from simulation import Simulation

class RootWidget(BoxLayout):
    policy_graph_33 = BooleanProperty(True)
    policy_graph_44 = BooleanProperty(False)
    policy_graph_55 = BooleanProperty(False)
    inputEpsilon = None
    inputNPeople = None
    inputNGrid = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def start_clicked(self):
        
        policy_graph_booleans = [self.policy_graph_33, self.policy_graph_44, self.policy_graph_55]
        if sum(policy_graph_booleans) == 0:
            self.text = "check any policy graph"
            return
        else:
            policy_graph_value = np.array([3,5,7])[tuple([policy_graph_booleans])][0]
            
        sim = Simulation(pop_size=int(self.inputNPeople.text), epsilon=float(self.inputEpsilon.text), n_grid=int(self.inputNGrid.text))
        print("run")
        sim.run()
        
        
class UiApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    UiApp().run()

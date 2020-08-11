from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
import numpy as np
import matplotlib.pyplot as plt
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
import sys
sys.path.append("../../")

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
            policy_graph_value = np.array([3,4,5])[tuple([policy_graph_booleans])][0]
            
        print(float(self.inputEpsilon.text))
        sim = Simulation(pop_size=int(self.inputNPeople.text), policy_graph=policy_graph_value, epsilon=float(self.inputEpsilon.text), n_grid=int(self.inputNGrid.text))
        print("run")
        sim.run()
        
""" 
class GraphView(BoxLayout):
    fig, ax = plt.subplots()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

        widget = FigureCanvasKivyAgg(GraphView.fig)
        self.add_widget(widget)

        Clock.schedule_interval(self.update_view, 0.01)

    def update_view(self, *args, **kwargs):
        GraphView.fig.canvas.draw()
        GraphView.fig.canvas.flush_events()
"""
        
class UiApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    UiApp().run()
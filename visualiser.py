'''
contains all methods for visualisation tasks
'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from environment import build_hospital
from utils import check_folder

def set_style(Config):
    '''sets the plot style
    
    '''
    if Config.plot_style.lower() == 'dark':
        mpl.style.use('plot_styles/dark.mplstyle')


def build_fig(Config, figsize=(9,5)):
    set_style(Config)
    #fig = plt.figure(figsize=(5,7))
    fig = plt.figure(figsize=figsize)
    spec = fig.add_gridspec(ncols=2, nrows=2, height_ratios=[5,5])
    #spec = fig.add_gridspec(ncols=1, nrows=1)

    ax1 = fig.add_subplot(spec[0,0])
    #plt.title('locations')
    #plt.xlim(Config.xbounds[0], Config.xbounds[1])
    #plt.ylim(Config.ybounds[0], Config.ybounds[1])
    ax1.set_title("locations")
    #ax1.set_xlim(Config.xbounds[0], Config.xbounds[1])
    #ax1.set_ylim(Config.ybounds[0], Config.ybounds[1])

    ax2 = fig.add_subplot(spec[1,0])
    ax2.set_title('perturbed locations')
    #ax2.set_xlim(Config.xbounds[0], Config.xbounds[1])
    #ax2.set_ylim(Config.ybounds[0], Config.ybounds[1])
    
    ax3 = fig.add_subplot(spec[0,1])
    ax3.set_title('number of contact')   
    ax4 = fig.add_subplot(spec[1,1])
    ax4.set_title('place holder')

    #if 

    return fig, spec, ax1, ax2, ax3, ax4
    #return fig, spec, ax1
            
#def draw_tstep(Config, population, pop_tracker, frame,
#               fig, spec, ax1, ax2):
#def draw_tstep(Config, perturbed_population, pop_tracker, frame,
#               fig, spec, ax1, ax2):
def draw_tstep(Config, population, perturbed_population, counts, perturbed_counts, e_distances, frame,
               fig, spec, ax1, ax2, ax3, ax4):
#def draw_tstep(Config, population, pop_tracker, frame,
#               fig, spec, ax1):
    #construct plot and visualise

    #set plot style
    set_style(Config)

    #get color palettes
    palette = Config.get_palette()

    #spec = fig.add_gridspec(ncols=2, nrows=2, height_ratios=[5,2])
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    ax1.set_xlim(Config.x_plot[0], Config.x_plot[1])
    ax1.set_ylim(Config.y_plot[0], Config.y_plot[1])
    ax2.set_xlim(Config.x_plot[0], Config.x_plot[1])
    ax2.set_ylim(Config.y_plot[0], Config.y_plot[1])
    view_range = 100
    ax3.set_xlim(frame-view_range, frame)
    ax3.set_ylim(-5, Config.pop_size + 5)
    ax3.set_ylabel("count")
    ax4.set_xlim(frame-view_range, frame)
    ax4.set_ylim(0, 0.5)
    ax4.set_xlabel("time step")
    ax4.set_ylabel("Average Euclidean distance")

    if Config.self_isolate and Config.isolation_bounds != None:
        build_hospital(Config.isolation_bounds[0], Config.isolation_bounds[2],
                       Config.isolation_bounds[1], Config.isolation_bounds[3], ax1,
                       addcross = False)
        
    ax1.scatter(population[:,1], population[:,2], color=palette[0], s = 2, label='locations')
    ax1.legend()
    #plot population segments
    #healthy = population[population[:,6] == 0][:,1:3]
    #ax1.scatter(healthy[:,0], healthy[:,1], color=palette[0], s = 2, label='healthy')
    
    #infected = population[population[:,6] == 1][:,1:3]
    #ax1.scatter(infected[:,0], infected[:,1], color=palette[1], s = 2, label='infected')

    #immune = population[population[:,6] == 2][:,1:3]
    #ax1.scatter(immune[:,0], immune[:,1], color=palette[2], s = 2, label='immune')
    
    #fatalities = population[population[:,6] == 3][:,1:3]
    #ax1.scatter(fatalities[:,0], fatalities[:,1], color=palette[3], s = 2, label='dead')
        
    
    #add text descriptors
    #ax1.text(Config.x_plot[0], 
    #         Config.y_plot[1] + ((Config.y_plot[1] - Config.y_plot[0]) / 100), 
    #         'timestep: %i, total: %i, healthy: %i infected: %i immune: %i fatalities: %i' %(frame,
    #                                                                                         len(population),
    #                                                                                         len(healthy), 
    #                                                                                         len(infected), 
    #                                                                                         len(immune), 
    #                                                                                         len(fatalities)),
    #            fontsize=6)
    ax1.text(Config.x_plot[0], Config.y_plot[1] + ((Config.y_plot[1] - Config.y_plot[0]) / 100), 'timestep: %i' %(frame))
    
    ax2.scatter(perturbed_population[:,1], perturbed_population[:,2], color=palette[0], s = 2, label='perturbed locations')
    ax2.legend()
    #healthy = perturbed_population[perturbed_population[:,6] == 0][:,1:3]
    #ax2.scatter(healthy[:,0], healthy[:,1], color=palette[0], s = 2, label='healthy')
    
    #infected = perturbed_population[perturbed_population[:,6] == 1][:,1:3]
    #ax2.scatter(infected[:,0], infected[:,1], color=palette[1], s = 2, label='infected')

    #immune = perturbed_population[perturbed_population[:,6] == 2][:,1:3]
    #ax2.scatter(immune[:,0], immune[:,1], color=palette[2], s = 2, label='immune')
    
    #fatalities = perturbed_population[perturbed_population[:,6] == 3][:,1:3]
    #ax2.scatter(fatalities[:,0], fatalities[:,1], color=palette[3], s = 2, label='dead')
        
    
    #ax2.set_title('number of infected')
    #ax2.text(0, Config.pop_size * 0.05, 
    #            'https://github.com/paulvangentcom/python-corona-simulation',
    #            fontsize=6, alpha=0.5)
    #ax2.set_xlim(0, simulation_steps)
    #ax2.set_ylim(0, Config.pop_size + 200)

    #if Config.treatment_dependent_risk:
    #    infected_arr = np.asarray(pop_tracker.infectious)
    #    indices = np.argwhere(infected_arr >= Config.healthcare_capacity)

        #ax2.plot([Config.healthcare_capacity for x in range(len(pop_tracker.infectious))], 
        #         'r:', label='healthcare capacity')

    #if Config.plot_mode.lower() == 'default':
        #ax2.plot(pop_tracker.infectious, color=palette[1])
        #ax2.plot(pop_tracker.fatalities, color=palette[3], label='fatalities')
    #elif Config.plot_mode.lower() == 'sir':
    #    ax2.plot(pop_tracker.susceptible, color=palette[0], label='susceptible')
    #    ax2.plot(pop_tracker.infectious, color=palette[1], label='infectious')
    #    ax2.plot(pop_tracker.recovered, color=palette[2], label='recovered')
    #    ax2.plot(pop_tracker.fatalities, color=palette[3], label='fatalities')
    #else:
    #    raise ValueError('incorrect plot_style specified, use \'sir\' or \'default\'')

    #ax2.legend(loc = 'best', fontsize = 6)
    ax3.plot(range(frame+1), counts, color=palette[0], label="counts")
    ax3.plot(range(frame+1), perturbed_counts[0], color=palette[1], label="privacy-preserved counts 3*3")
    ax3.plot(range(frame+1), perturbed_counts[1], color=palette[2], label="privacy-preserved counts 4*4")
    ax3.plot(range(frame+1), perturbed_counts[2], color=palette[3], label="privacy-preserved counts 5*5")
    ax3.legend(fontsize=6)

    ax4.plot(range(frame+1), e_distances[0], color=palette[1], label="3*3")
    ax4.plot(range(frame+1), e_distances[1], color=palette[2], label="4*4")
    ax4.plot(range(frame+1), e_distances[2], color=palette[3], label="5*5")
    ax4.legend()
    
    plt.draw()
    plt.pause(0.0001)

    if Config.save_plot:
        try:
            plt.savefig('%s/%i.png' %(Config.plot_path, frame))
        except:
            check_folder(Config.plot_path)
            plt.savefig('%s/%i.png' %(Config.plot_path, frame))
            
def plot_sir(Config, pop_tracker, size=(6,3), include_fatalities=False,
             title='S-I-R plot of simulation'):
    '''plots S-I-R parameters in the population tracker
    
    Keyword arguments
    -----------------
    Config : class
        the configuration class
        
    pop_tracker : ndarray
        the population tracker, containing
        
    size : tuple
        size at which the plot will be initialised (default: (6,3))
        
    include_fatalities : bool
        whether to plot the fatalities as well (default: False) 
    '''
    
    #set plot style
    set_style(Config)

    #get color palettes
    palette = Config.get_palette()
    
    #plot the thing
    plt.figure(figsize=size)
    plt.title(title)    
    plt.plot(pop_tracker.susceptible, color=palette[0], label='susceptible')
    plt.plot(pop_tracker.infectious, color=palette[1], label='infectious')
    plt.plot(pop_tracker.recovered, color=palette[2], label='recovered')
    if include_fatalities:
        plt.plot(pop_tracker.fatalities, color=palette[3], label='fatalities')
        
    #add axis labels
    plt.xlabel('time in hours')
    plt.ylabel('population')
    
    #add legend
    plt.legend()
    
    #beautify
    plt.tight_layout()
    
    #initialise
    plt.show()

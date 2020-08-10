import numpy as np

def surveil(states):
    counter = 0

    for i, state in enumerate(states):
        if state in np.concatenate([states[:i], states[i+1:]]):
            counter += 1
    return counter
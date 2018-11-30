"""
This module randomly generates link capacity for each link.
"""
import os
import numpy as np
np.random.seed(2)


def generate_capacity(links, lower_bound=5000, upper_bound=5001):
    """
    NOTE: You should ensure the input links contains bidirectional edges.
    """
    return np.random.randint(lower_bound, upper_bound, (len(links),), dtype=np.int).tolist()


def save_capacity(capacity, data_dir='data/', fmt='.dat'):
    if fmt == '.dat':
        fp = open(os.path.join(data_dir, 'capacity.dat'), 'w')
        fp.write('Capacity = {};'.format(str(capacity)))
        fp.close()
    elif fmt == '.pickle':
        import pickle
        fp = open(os.path.join(data_dir, 'capacity.pickle'), 'w')
        pickle.dump(capacity, fp)
        fp.close()

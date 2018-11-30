"""
This module is used for generating traffic demand matrix from all source-destination pairs.
"""
import os
import numpy as np
np.random.seed(1)


def generate_demand_mat(nodes, lower_bound=50, upper_bound=100, loc=75, scale=10, dist='uniform'):
    num_nodes = len(nodes)

    demand_mat = None
    if dist == 'uniform':
        demand_mat = np.random.randint(lower_bound, upper_bound, (num_nodes, num_nodes), dtype=np.int)
    elif dist == 'norm':
        demand_mat = np.random.normal(loc, scale, (num_nodes, num_nodes))
        demand_mat = demand_mat.astype(np.int)
        demand_mat[demand_mat < 0] = 0

    mask = np.eye(num_nodes, num_nodes, dtype=np.bool)
    demand_mat *= np.logical_not(mask)
    meta = {'total': np.sum(demand_mat),
            'max': np.max(demand_mat),
            'min': np.min(demand_mat + np.eye(num_nodes, num_nodes, dtype=np.int)*np.max(demand_mat))}
    return demand_mat, meta


def save_demand_mat(demand_mat, data_dir='data/', fmt='.dat'):
    """
    NOTE: Assignment the demand to source-destination pairs.
    """
    if fmt == '.dat':
        demand_k = demand_mat.flatten()
        demand_k = demand_k[demand_k.nonzero()].tolist()
        fp = open(os.path.join(data_dir, 'demand.dat'), 'w')
        fp.write('Demands = {};'.format(str(demand_k)))
        fp.close()
    elif fmt == '.pickle':
        import pickle
        fp = open(os.path.join(data_dir, 'demand.pickle'), 'w')
        pickle.dump(demand_mat, fp)
        fp.close()

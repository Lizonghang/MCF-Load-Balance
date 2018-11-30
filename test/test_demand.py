import sys
sys.path.append('../')

from demand import generate_demand_mat
from demand import save_demand_mat
from graph import load_graph


if __name__ == "__main__":
    G = load_graph(data_dir='../data')
    nodes = G.nodes.keys()
    demand_mat, meta = generate_demand_mat(nodes, dist='norm')
    save_demand_mat(demand_mat, data_dir='../data')
    print 'You can set link capacity to alpha *', meta['total'], 'alpha located in (0.5, 1.0).'

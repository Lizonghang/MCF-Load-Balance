import sys
sys.path.append('../')

from graph import load_graph
from graph import draw_graph
from ksp import k_shortest_paths

if __name__ == "__main__":
    G = load_graph(data_dir='../data')
    nodes = G.nodes.keys()
    paths = k_shortest_paths(G, s=1, t=11, kmax=5)
    print 'top k shortest paths are:'
    for idx, p in enumerate(paths):
        print idx+1, ":", p
    draw_graph(G)

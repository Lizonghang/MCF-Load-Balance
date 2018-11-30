import sys
sys.path.append('../')

from delta import make_bidlinks
from delta import generate_delta
from delta import save_delta
from graph import load_graph
from candidate import generate_candidate_paths


if __name__ == "__main__":
    G = load_graph('../data')
    links = G.edges.keys()
    make_bidlinks(links)
    paths = generate_candidate_paths(G, kmax=10)
    delta = generate_delta(links, paths)
    save_delta(delta, data_dir='../data')

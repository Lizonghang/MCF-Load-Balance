import sys
sys.path.append('../')

from graph import load_graph
from delta import make_bidlinks
from capacity import generate_capacity
from capacity import save_capacity


if __name__ == "__main__":
    G = load_graph('../data')
    links = G.edges.keys()
    make_bidlinks(links)
    capacity = generate_capacity(links)
    save_capacity(capacity, '../data', '.dat')
    save_capacity(capacity, '../data', '.pickle')

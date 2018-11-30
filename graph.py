"""
This module loads data from nodes.txt and links.txt, creates and returns networkx.Graph() object.
"""
import networkx as nx
import matplotlib.pyplot as plt
import os


def load_graph(data_dir='data'):
    nodes_path = os.path.join(data_dir, 'nodes.txt')
    links_path = os.path.join(data_dir, 'links.txt')
    assert os.path.exists(nodes_path)
    assert os.path.exists(links_path)

    nodes = []
    links = []
    with open(nodes_path, 'r') as fp:
        nodes += map(int, fp.readlines())
    with open(links_path, 'r') as fp:
        links += map(lambda r: map(int, r.split()), fp.readlines())

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(links)
    return G


def draw_graph(G, edge_labels=None):
    plt.figure()
    nx.draw(G, pos=nx.circular_layout(G), with_labels=True, font_weight='bold')
    if edge_labels:
        nx.draw_networkx_edge_labels(
            G,
            pos=nx.circular_layout(G),
            font_size=10,
            edge_labels=edge_labels
        )

import sys
sys.path.append('../')
import matplotlib.pyplot as plt

from graph import load_graph
from graph import draw_graph


if __name__ == "__main__":
    G = load_graph(data_dir='../data')
    draw_graph(G)
    plt.show()

"""
This module convert the raw data in data_dir to .dat format.
"""
import os
from delta import make_bidlinks


def txt2dat(data_dir='data', kmax=10):
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

    make_bidlinks(links)

    fp = open(os.path.join(data_dir, 'base.dat'), 'w')
    fp.write('NumNodes = {};'.format(len(nodes)) + '\n')
    fp.write('NumLinks = {};'.format(len(links)) + '\n')
    fp.write('NumPaths = {};'.format(kmax))
    fp.close()

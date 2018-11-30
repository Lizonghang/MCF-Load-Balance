"""
This module generate the incidence matrix (delta) between links and paths.
"""
import os
import numpy as np


def generate_delta(links, paths):
    """
    NOTE:
        1. You should ensure the input links contains bidirectional edges.
        2. You should ensure the number of candidate paths for each source-destination pair is the same,
           otherwise the size of each depth in matrix delta may be mismatching. You can save the paths as
           dat format and check whether the numbers in data/num_paths.dat are the same.
    """
    num_links = len(links)
    num_paths = 0
    num_pairs = 0

    # calculate number of paths for each source-destination pair
    # check whether the number of paths for all pairs are the same
    for s in paths:
        for t in paths[s]:
            num_pairs += 1
            if num_paths == 0:
                num_paths = len(paths[s][t])
            else:
                assert num_paths == len(paths[s][t])

    # initial incidence matrix
    delta = np.zeros((num_pairs, num_links, num_paths), dtype=np.int)

    # fill values of delta
    k = -1
    for s in paths:
        for t in paths[s]:
            k += 1
            # for each commodity flow
            for l in xrange(num_links):
                for p in xrange(num_paths):
                    # check whether link exists in path
                    if is_link_in_path(links[l], paths[s][t][p]['path']):
                        delta[k][l][p] = 1

    return delta


def make_bidlinks(links):
    num = len(links)
    for i in xrange(num):
        links.append(links[i][::-1])


def is_link_in_path(link, path):
    try:
        return path[path.index(link[0])+1] == link[1]
    except (IndexError, ValueError):
        return False


def save_delta(delta, data_dir='data/'):
    fp = open(os.path.join(data_dir, 'delta.dat'), 'w')
    fp.write('Delta = [' + '\n')
    num_pairs, num_links, num_paths = delta.shape
    for k in xrange(num_pairs):
        fp.write('    [')
        for l in xrange(num_links):
            fp.write('[{}]{}'.format(','.join(map(str, delta[k][l].tolist())),
                                     '' if l == num_links-1 else ',\n     '))
        fp.write('],' + '\n')
    fp.write('];')
    fp.close()

"""
This module is used to generate candidate paths for all source-destination
pairs by iteratively call top-k-shortest-path algorithm.
"""
from ksp import k_shortest_paths
import os


def generate_candidate_paths(G, kmax=10):
    nodes = G.nodes.keys()
    candidate_paths = {}
    # initial candidate paths
    for s in nodes:
        for t in nodes:
            if s != t: candidate_paths[s] = {t: None}
    # fill the paths
    for i in xrange(len(nodes)):
        s = nodes[i]
        for j in xrange(i+1, len(nodes)):
            t = nodes[j]
            paths = k_shortest_paths(G, s, t, kmax)
            candidate_paths[s][t] = paths
            # due to symmetry, candidate_paths[t][s] is the same as candidate_paths[s][t], but in reverse order.
            reversed_paths = {}
            for i in xrange(len(paths)):
                reversed_paths[i] = {}
                reversed_paths[i]['cost'] = paths[i]['cost']
                reversed_paths[i]['path'] = paths[i]['path'][::-1]
            candidate_paths[t][s] = reversed_paths
    return candidate_paths


def save_candidate_paths(candidate_paths, filename='data/paths.dat'):
    filepath, filename = os.path.split(filename)
    fn_prefix, fn_ext = os.path.splitext(filename)
    if fn_ext == '.json':
        import json
        json_str = json.dumps(candidate_paths)
        with open(os.path.join(filepath, filename), 'w') as fp:
            fp.write(json_str)
    elif fn_ext == '.dat':
        # save detail paths between source-termination pairs
        fp = open(os.path.join(filepath, filename), 'w')
        fp.write('Paths = #[' + '\n')
        for s in candidate_paths:
            fp.write('\t{}: #['.format(s) + '\n')
            for t in candidate_paths[s]:
                fp.write('\t\t{}: ['.format(t))
                num_path = len(candidate_paths[s][t])
                for i in xrange(num_path):
                    path = candidate_paths[s][t][i]['path']
                    if i != num_path-1:
                        fp.write('[' + ','.join(map(str, path)) + '],' + '\n')
                        fp.write('\t\t    ' + ' ' * (t/10))
                    else:
                        fp.write('[' + ','.join(map(str, path)) + ']')
                fp.write(']' + '\n')
            fp.write('\t]#' + '\n')
        fp.write(']#;')
        fp.close()

        # save count of paths between source-termination pairs
        fp = open(os.path.join(filepath, 'num_' + filename), 'w')
        fp.write('NumPaths = #[' + '\n')
        for s in candidate_paths:
            fp.write('\t{}: #['.format(s))
            for t in candidate_paths[s]:
                fp.write('\t{}: {}'.format(t, len(candidate_paths[s][t])))
            fp.write('\t]#' + '\n')
        fp.write(']#;')
        fp.close()

        # save count of nodes in each paths between source-destination pairs
        fp = open(os.path.join(filepath, 'num_nodes_in_' + filename), 'w')
        fp.write('NumNodesInEachPath = #[' + '\n')
        for s in candidate_paths:
            fp.write('\t{}: #['.format(s) + '\n')
            for t in candidate_paths[s]:
                fp.write('\t\t{}: ['.format(t))
                num_path = len(candidate_paths[s][t])
                for i in xrange(num_path):
                    path = candidate_paths[s][t][i]['path']
                    fp.write('{}{}'.format(len(path), '' if i==num_path-1 else ','))
                fp.write(']' + '\n')
            fp.write('\t]#' + '\n')
        fp.write(']#;')
        fp.close()
    elif fn_ext == '.pickle':
        import pickle
        fp = open(os.path.join(filepath, filename), 'w')
        pickle.dump(candidate_paths, fp)
        fp.close()
    else:
        print 'Save failed, unsupported format.'

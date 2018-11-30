import sys
sys.path.append('../')

from graph import load_graph
from candidate import generate_candidate_paths
from candidate import save_candidate_paths

if __name__ == "__main__":
    G = load_graph(data_dir='../data')
    candidate_paths = generate_candidate_paths(G, kmax=10)

    # check if the paths are sorted by cost, if not, something wrong happens in KSP algorithm.
    for s in candidate_paths:
        for t in candidate_paths[s]:
            num_paths = len(candidate_paths[s][t])
            for i in xrange(num_paths-1):
                assert candidate_paths[s][t][i]['cost'] <= candidate_paths[s][t][i+1]['cost']

    # check if the count of actual paths is equal to N(N-1)
    num_total_paths = 0
    for s in candidate_paths:
        for t in candidate_paths[s]:
            num_total_paths += 1
            # print 'candidate paths from {} to {}:'.format(s, t)
            # for p in candidate_paths[s][t]:
            #     print '  ', p
    num_nodes = len(G.nodes.keys())
    assert num_total_paths == num_nodes * (num_nodes - 1)

    # save to file
    save_candidate_paths(candidate_paths, filename='../data/paths.dat')

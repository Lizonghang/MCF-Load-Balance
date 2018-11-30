"""
This module calculates the top-k-shortest-paths using YenKSP algorithm.
"""
import networkx as nx


def k_shortest_paths(G, s, t, kmax):
    assert s in G.nodes
    assert t in G.nodes

    G_ = G.copy()
    try:
        # Assume the weights of links are all 1.
        shortest_path = nx.shortest_path(G_, s, t)
        distances = initial_distances(shortest_path)
    except nx.exception.NetworkXNoPath:
        return {'cost': 0, 'path': []}

    # k shortest paths, sorted by cost
    A = [{'cost': distances[t], 'path': shortest_path}]
    # initialize the set to store the potential kth shortest path.
    B = []

    for k in range(1, kmax):
        distances = distances if k == 1 else update_distances(A[-1]['path'])
        # the spur node ranges from the first node to the next to last node in the previous k-shortest path.
        for i in range(0, len(A[-1]['path'])-1):
            # spur node is retrieved from the previous k-shortest path, k - 1.
            node_spur = A[-1]['path'][i]
            # The sequence of nodes from the source to the spur node of the previous k-shortest path.
            path_root = A[-1]['path'][:i+1]

            # remove the links that are part of the previous shortest paths which share the same root path.
            for path_json in A:
                path = path_json['path']
                if len(path) > i and path_root == path[:i+1]:
                    try:
                        G_.remove_edge(path[i], path[i+1])
                    except nx.exception.NetworkXError:
                        continue
            # remove the nodes that are part of the path from root to the spur node, except spur node.
            for node in path_root[:-1]:
                G_.remove_node(node)

            # calculate the spur path from the spur node to the sink.
            try:
                path_spur = nx.shortest_path(G_, node_spur, t)
            except nx.exception.NetworkXNoPath:
                path_spur = []

            if path_spur:
                # entire path is made up of the root path and spur path.
                path_total = path_root[:-1] + path_spur
                dist_total = distances[node_spur] + len(path_spur) - 1
                potential_path = {'cost': dist_total, 'path': path_total}
                # add the potential k-shortest path to the heap.
                if not (potential_path in B):
                    B.append(potential_path)

            # add back the edges and nodes that were removed from the graph.
            # here we delete the copy of G and assign G_ with G.
            del G_
            G_ = G.copy()

        # this handles the case of there being no spur paths, or no spur paths left.
        # this could happen if the spur paths have already been exhausted (added to A),
        # or there are no spur paths at all - such as when both the source and sink vertices
        # lie along a "dead end".
        if not B: break

        # sort the potential k-shortest paths by cost.
        B = sorted(B, key=lambda x: x['cost'])
        # add the lowest cost path becomes the k-shortest path.
        A.append(B[0])
        # remove the shortest potential path from the potential path set
        B.pop(0)

    return A


def initial_distances(path):
    distances = {}
    for cost, node in enumerate(path):
        distances[node] = cost
    return distances


def update_distances(path):
    distances = {path[0]: 0}
    cost = 0
    for i in range(len(path)-1):
        cost += 1
        distances[path[i+1]] = cost
    return distances

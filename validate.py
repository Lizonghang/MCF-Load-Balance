#!/usr/bin/env python
"""
This module validates the solution of cplex/mcf.mod and compares the performance of random seleted paths from
top-k-shortest paths, shortest paths and cplex optimized paths. The link distributions of range link utilization
rate are figured below.
"""
import os
import re
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt
from graph import load_graph
from graph import draw_graph
from delta import make_bidlinks
from prepare import kmax

import warnings
warnings.filterwarnings("ignore")

data_dir = 'data/'
cplex_dir = 'cplex/'


def parse_solution(solution):
    z = round(float(re.findall(r'z = ([0-9.]+);', solution)[0]), 3)
    dvars = map(lambda xp: map(int, xp.split()), re.findall(r'\[([01 ]+)\]', solution))
    return z, dvars


def get_links_in_path(path):
    links = []
    for i in xrange(len(path)-1):
        links.append((path[i], path[i+1]))
    return links


def exec_route(links, capacity, route):
    # initial link utilization rate map
    link_util = {}
    for link in links:
        link_util[link] = 0.

    # aggregate flow demands
    for s in route:
        for t in route[s]:
            path = route[s][t]['path']
            demand = route[s][t]['demand']
            for link in get_links_in_path(path):
                link_util[link] += demand

    # calculate link capacity utilization rate
    for idx, link in enumerate(links):
        link_util[link] /= capacity[idx]
        link_util[link] = round(link_util[link], 3)

    return link_util


def draw_dist(link_util, interval=0.1, prefix=''):
    vals = link_util.values()
    val_max = max(max(vals), 1.)
    num_bucket = int(val_max / interval)
    bucket = [0 for _ in xrange(num_bucket)]
    for val in link_util.values():
        bucket[int(val / interval)] += 1

    val_sum = sum(bucket)
    for i in xrange(len(bucket)):
        bucket[i] /= float(val_sum)

    plt.figure()
    plt.bar(np.arange(0, len(bucket)) * interval, bucket, width=interval)
    plt.title('[{}] Distribution of Link Utilization Rate.'.format(prefix))
    plt.xlabel('Link Utilization Rate')
    plt.ylabel('Ratio of Link Count')
    plt.xlim(0., 1.)
    plt.ylim(0., 0.5)
    plt.grid()


def eval_cplex_lp(links, paths, capacity, demand_k, draw=False):
    # parse solution
    fp = open(os.path.join(cplex_dir, 'solution.txt'), 'r')
    solution = ''.join(fp.readlines())
    fp.close()
    z, dvars = parse_solution(solution)

    # initial route to store paths and demands
    route = {}
    for s in paths:
        route[s] = {}
        for t in paths[s]:
            route[s][t] = {}

    # fill values to route
    k = -1
    for s in paths:
        for t in paths[s]:
            k += 1
            p = dvars[k].index(1)
            route[s][t]['path'] = paths[s][t][p]['path']
            route[s][t]['demand'] = demand_k[k]

    # calculate link capacity utilization rate
    link_util = exec_route(links, capacity, route)

    if draw:
        # draw graph with link utilization rate
        edge_labels = {}
        for edge in G.edges:
            i, j = edge
            if i > j: i, j = j, i
            edge_labels[edge] = '({}%/{}%)'.format(
                i, j, link_util[(i, j)]*100,
                j, i, link_util[(j, i)]*100
            )
        draw_graph(G, edge_labels)

        # draw distribution of link utilization rate
        draw_dist(link_util, interval=0.1, prefix='CPLEX ROUTE')

    link_max = None
    util_max = 0.
    for link in link_util:
        if link_util[link] >= util_max:
            util_max = link_util[link]
            link_max = link

    assert util_max == z, 'util_max={},z={}'.format(util_max, z)
    return util_max, link_max


def eval_shortest_route(links, paths, capacity, demand_k, draw=False):
    # initial route to store paths and demands
    route = {}
    for s in paths:
        route[s] = {}
        for t in paths[s]:
            route[s][t] = {}

    # fill values to route
    k = -1
    for s in paths:
        for t in paths[s]:
            k += 1
            route[s][t]['path'] = paths[s][t][0]['path']
            route[s][t]['demand'] = demand_k[k]

    # calculate link capacity utilization rate
    link_util = exec_route(links, capacity, route)

    if draw:
        # draw distribution of link utilization rate
        draw_dist(link_util, interval=0.1, prefix='SHORTEST ROUTE')

    link_max = None
    util_max = 0.
    for link in link_util:
        if link_util[link] >= util_max:
            util_max = link_util[link]
            link_max = link
    return util_max, link_max


def eval_random_route(links, paths, capacity, demand_k, draw=False):
    np.random.seed(int(time.time()))
    # initial route to store paths and demands
    route = {}
    for s in paths:
        route[s] = {}
        for t in paths[s]:
            route[s][t] = {}

    # fill values to route
    k = -1
    for s in paths:
        for t in paths[s]:
            k += 1
            p = np.random.randint(0, kmax)
            route[s][t]['path'] = paths[s][t][p]['path']
            route[s][t]['demand'] = demand_k[k]

    # calculate link capacity utilization rate
    link_util = exec_route(links, capacity, route)

    del route

    if draw:
        # draw distribution of link utilization rate
        draw_dist(link_util, interval=0.1, prefix='RANDOM ROUTE')

    link_max = None
    util_max = 0.
    for link in link_util:
        if link_util[link] >= util_max:
            util_max = link_util[link]
            link_max = link
    return util_max, link_max


def compare_performance(links, paths, capacity, demand_k, draw=True):
    performance = {}

    util_max, link_max = eval_cplex_lp(links, paths, capacity, demand_k, draw)
    performance['cplex_route'] = util_max
    print '[CPLEX ROUTE] Maximum link utilization,',
    print '({},{}): {}'.format(link_max[0], link_max[1], util_max)
    print '[CPLEX ROUTE] Capacity:',
    print '({},{}): {}'.format(link_max[0], link_max[1], capacity[links.index(link_max)])

    util_max, link_max = eval_shortest_route(links, paths, capacity, demand_k, draw)
    performance['shortest_route'] = util_max
    print '[SHORTEST ROUTE] Maximum link utilization,',
    print '({},{}): {}'.format(link_max[0], link_max[1], util_max)
    print '[SHORTEST ROUTE] Capacity:',
    print '({},{}): {}'.format(link_max[0], link_max[1], capacity[links.index(link_max)])

    util_max, link_max = eval_random_route(links, paths, capacity, demand_k, draw)
    performance['random_route'] = util_max
    print '[RANDOM ROUTE] Maximum link utilization,',
    print '({},{}): {}'.format(link_max[0], link_max[1], util_max)
    print '[RANDOM ROUTE] Capacity:',
    print '({},{}): {}'.format(link_max[0], link_max[1], capacity[links.index(link_max)])

    if draw:
        plt.show()

    return performance


def check_optimal(links, paths, capacity, demand_k, cplex_route_util):
    min_util_max = 1.
    iteration = 0
    while min_util_max >= cplex_route_util:
        iteration += 1
        util_max, link_max = eval_random_route(links, paths, capacity, demand_k, draw=False)
        if util_max < min_util_max:
            min_util_max = util_max
            print '[Iteration {}] current: {}, optimal: {}'\
                .format(iteration, min_util_max, cplex_route_util)
            assert cplex_route_util <= min_util_max


if __name__ == "__main__":
    # prepare data: links, paths, capacity, demand
    # load links
    G = load_graph(data_dir)
    links = G.edges.keys()
    make_bidlinks(links)
    # load paths
    fp = open('data/paths.pickle', 'r')
    paths = pickle.load(fp)
    fp.close()
    # load capacity
    fp = open(os.path.join(data_dir, 'capacity.pickle'), 'r')
    capacity = pickle.load(fp)
    fp.close()
    # load demand matrix
    fp = open(os.path.join(data_dir, 'demand.pickle'), 'r')
    demand_mat = pickle.load(fp)
    fp.close()
    # align demand to dvars
    demand_k = demand_mat.flatten()
    demand_k = demand_k[demand_k.nonzero()].tolist()

    # compare performance of:
    #     * Random Selected Paths (from top-k-shortest-paths)
    #     * Shortest-Paths
    #     * CPLEX Optimized Paths.
    performance = compare_performance(links, paths, capacity, demand_k, draw=True)

    # check if MIP solution is optimal
    # check_optimal(links, paths, capacity, demand_k, performance['cplex_route'])

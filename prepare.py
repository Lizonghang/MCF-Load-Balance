#!/usr/bin/env python
"""
This function prepares data for cplex optimization. The files will be saved to data/ and then copied to cplex/.
Data includes:
    1. base.dat: includes NumNodes, NumLinks, NumPaths.
    2. paths.dat: includes Paths. Specify the selected candidate paths for each source-destination pair.
    3. num_nodes_in_paths.dat(optional): includes NumNodesInEachPath. Specify the number of nodes contained in each path.
    4. num_paths.dat(optional): includes NumPaths. Specify the number of paths contained in each source-destination pair.
    5. demand.dat: includes Demands. Specify the demand matrix.
    6. delta.dat: includes Delta. Specify the incidence matrix between links and paths. The values are 0 or 1.
    7. capacity.dat: includes Capacity. Specify the link capacity for each link.
Only the data which are needed by cplex optimizer is copied to cplex/, including:
    1. base.dat
    2. demand.dat
    3. capacity.dat
    4. delta.dat
Copy cplex/mcf.mod and cplex/*.dat to your OPL project, solve the LP problem, paste the solution to cplex/solution.txt,
and runs:
    python validate.py
or
    ./validate.py
to visualize the flows on the graph and the distribution of link capacity utilization rate.
"""
import os
import shutil
from graph import load_graph
from txt2dat import txt2dat
from candidate import generate_candidate_paths
from candidate import save_candidate_paths
from demand import generate_demand_mat
from demand import save_demand_mat
from delta import generate_delta
from delta import save_delta
from delta import make_bidlinks
from capacity import generate_capacity
from capacity import save_capacity


# global settings
data_dir = 'data/'
cplex_dir = 'cplex/'
kmax = 5


if __name__ == "__main__":
    print '[LOG] Preparing Data ...'
    # generate base.dat
    txt2dat(data_dir, kmax)
    # generate paths.dat, num_nodes_in_paths.dat, num_paths.dat
    G = load_graph(data_dir)
    candidate_paths = generate_candidate_paths(G, kmax)
    save_candidate_paths(candidate_paths, filename=os.path.join(data_dir, 'paths.dat'))
    save_candidate_paths(candidate_paths, filename=os.path.join(data_dir, 'paths.pickle'))
    # generate demand.dat
    nodes = G.nodes.keys()
    demand_mat, meta = generate_demand_mat(nodes, dist='norm')
    save_demand_mat(demand_mat, data_dir, fmt='.dat')
    save_demand_mat(demand_mat, data_dir, fmt='.pickle')
    # generate delta.dat
    links = G.edges.keys()
    make_bidlinks(links)
    delta = generate_delta(links, candidate_paths)
    save_delta(delta, data_dir)
    # generate capacity.dat
    capacity = generate_capacity(links)
    save_capacity(capacity, data_dir, '.dat')
    save_capacity(capacity, data_dir, '.pickle')
    print '[LOG] Data Created'

    # copy data/*.dat to cplex/
    register_dat_files = ['base.dat', 'demand.dat', 'delta.dat', 'capacity.dat']
    for filename in register_dat_files:
        shutil.copyfile(os.path.join(data_dir, filename), os.path.join(cplex_dir, filename))
    print '[LOG] Data Ready'

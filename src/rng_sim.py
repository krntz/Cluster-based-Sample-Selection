import sys, os
from shutil import copy2
import networkx as nx
import matplotlib.pyplot as plt
import cluster
import numpy as np
import random

# graph globals
G = nx.Graph()

bridge_vectors = set([])

def create_nodes(images, sm, c):
    for i in range(len(images)):
        G.add_node(images[i])
        G.node[images[i]]['cluster'] = c.labels_[i]

def create_edges(images, sm):
    # create edges between nodes with highest similarity score
    np.fill_diagonal(sm, 0.0)

    for i in range(len(images)):
        max_sim, = np.where(sm[i] == max(sm[i]))
        G.add_edge(images[i], images[max_sim[0]])

def mkdir_s(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    dir_name = sys.argv[1]
    in_dir = os.path.join(dir_name, 'in')
    gt_dir = os.path.join(dir_name, 'gt')

    images = os.listdir(in_dir)

    sm = cluster.build_similarity_matrix(in_dir, images)
    c = cluster.create_cluster(sm)

    create_nodes(images, sm, c)
    create_edges(images, sm)

    print("Finding bridge vectors")
    for edge in G.edges:
        n1 = edge[0]
        n2 = edge[1]

        if G.node[n1]['cluster'] != G.node[n2]['cluster']:
            bridge_vectors.add(n1)
            bridge_vectors.add(n2)

    results = len(bridge_vectors)/len(G.nodes)
    print("Removed %d%% of nodes" % (100-(results*100)))

    output_path = os.path.join('.', 'output')
    output_in = os.path.join(output_path, 'in')
    output_gt = os.path.join(output_path, 'gt')

    mkdir_s(os.path.join(output_path))
    mkdir_s(os.path.join(output_in))
    mkdir_s(os.path.join(output_gt))

    counter = 0
    for i in bridge_vectors:
        name = str(counter) + "_in.png"
        copy2(os.path.join(in_dir, i), os.path.join(output_in, name))
        copy2(os.path.join(gt_dir, i.replace('in', 'gt')), os.path.join(output_gt, name.replace('in', 'gt')))
        counter += 1

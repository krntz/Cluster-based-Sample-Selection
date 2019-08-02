import sys, os
from shutil import copy2
import networkx as nx
import matplotlib.pyplot as plt
import cluster
import numpy as np
import cv2
import math

# graph globals
G = nx.Graph()

bridge_vectors = set([])

def neighbors(dm, n1, n2):
    for n in G:
        if max(dm[n1][n], dm[n2][n]) < dm[n1][n2]:
            return False
    return True

def mkdir_s(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def load_images(files, dir_name):
    images = []

    for f in files:
        images.append(cv2.imread(os.path.join(dir_name, f), cv2.IMREAD_GRAYSCALE))

    return images

def build_distance_matrix(dir_name, images):
    num_images = len(images)
    dm = np.zeros(shape=(num_images, num_images), dtype=np.float64)

    print("Building distance matrix for %d images" % num_images)
    k = 0
    for i in range(dm.shape[0]):
        print("Calculating distances for image %d/%d" % (i+1, num_images), end='\r')
        for j in range(i+1, dm.shape[1]):
            dm[i][j] = math.sqrt(np.sum((images[i] - images[j])**2))

    print()
    dm = dm + dm.T
    np.fill_diagonal(dm, 0.0)
    
    return dm

if __name__ == "__main__":
    dir_name = sys.argv[1]
    in_dir = os.path.join(dir_name, 'in')
    gt_dir = os.path.join(dir_name, 'gt')

    image_files = os.listdir(in_dir)

    print("loading images")
    images = load_images(image_files, in_dir)

    sm = cluster.build_similarity_matrix(in_dir, image_files)
    dm = build_distance_matrix(in_dir, images)
    c = cluster.create_cluster(sm)

    print("Building RNG")
    count = 0
    for i in images:
        G.add_node(count)
        G.node[count]['im'] = i
        G.node[count]['cluster'] = c.labels_[count]
        count += 1

    for n1 in G:
        print("Finding neighbours for node %d/%d" % (n1+1, len(G)), end='\r')
        for n2 in G:
            if n1 < n2 and neighbors(dm, n1, n2):
                G.add_edge(n1, n2)

    print()
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
        copy2(os.path.join(in_dir, image_files[i]), os.path.join(output_in, name))
        copy2(os.path.join(gt_dir, image_files[i].replace('in', 'gt')), os.path.join(output_gt, name.replace('in', 'gt')))
        counter += 1

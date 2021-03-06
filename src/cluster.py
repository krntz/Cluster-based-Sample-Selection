import os, sys
import math
import datetime
import cv2
import numpy as np
from skimage.measure import compare_ssim as ssim
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt

def get_image_similarity(img1, img2):
    i1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
    i2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)

    similarity = 0.0

    similarity = ssim(i1, i2)

    return similarity

# calculate the SSIM index for every image pair
def build_similarity_matrix(dir_name, images):
    num_images = len(images)
    sm = np.zeros(shape=(num_images, num_images), dtype=np.float64)

    print("Building the similarity matrix for %d images" % num_images)

    k = 0
    for i in range(sm.shape[0]):
        print("Calculating similarities for image %d/%d" % (i+1, num_images), end='\r')
        for j in range(i+1, sm.shape[1]):
            sm[i][j] = get_image_similarity('%s/%s' % (dir_name, images[i]),
                                                '%s/%s' % (dir_name, images[j]))

    sm = sm + sm.T
    np.fill_diagonal(sm, 1.0)

    print("Done")
    return sm

# CAUTION! Do not use this method with large datasets!
def plot_similarity_matrix(m, images):
    fig, ax = plt.subplots(figsize=(20,20))
    cax = ax.matshow(m, interpolation=None)
    ax.grid(True)
    plt.xticks(range(len(images)), images, rotation=90)
    plt.yticks(range(len(images)), images)
    fig.colorbar(cax, ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, .80, .90, 1])
    plt.show()

def create_cluster(m):
    sc = AffinityPropagation(affinity='precomputed').fit(m)
    print("Number of clusters: %d" % len(set(sc.labels_)))

    return sc

if __name__ == "__main__":
    dir_name = sys.argv[1]
    images = os.listdir(dir_name)

    sm = build_similarity_matrix(dir_name, images)
    #plot_similarity_matrix(sm, images)

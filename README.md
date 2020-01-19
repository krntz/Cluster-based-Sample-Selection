# Cluster-based Sample Selection for Document Image Binarization

This repository accompanies the following paper:

A. Krantz and F. Westphal, “Cluster-Based Sample Selection for Document Image Binarization,” in
*2019 International Conference on Document Analysis and Recognition Workshops (ICDARW)*, 2019,
vol. 5, pp. 47–52.

A description of how to use it can be found in the `src` folder. 
The raw data (Psuedo F-Measure values) from the performed experiments can be found in `results.csv` and binarized images can be found in the `images` folder.

## Note on reuse and/or redistribution of code and/or data

You are free to use the code and/or data (i.e. anything in the repository that is not code, including but not limited to images and test results) in this repository (either all of it or parts of it) for personal use, academic research, teaching, or other academic/scholarly pursuits as long as the above paper is cited. For any other use cases not covered here (Including but not limited to business or enterprise), please contact me before using the code and/or data present in this repository.

## Running

Download the files in the `src` folder and use python 3 ro run either `rng_euc.py` or `rng_sim.py` depending the similarity metric that is to be used for the relative neighbourhood graph. Both files takes as input a folder containing the input images and their ground truth data.

The input folder must have the following structure:

```
input
|
+-- in
|   + *_in.png
+-- gt
    + *_gt.png
```

The reduced dataset will be placed in a folder named `output` with the same structure as the `input` folder.

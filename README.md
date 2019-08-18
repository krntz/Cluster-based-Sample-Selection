# Cluster-based Sample Selection for Document Image Binarization

This repository contains the implementation of the approach proposed in this paper. A description of how to use it can be found in the `src` folder. 
The raw data from the performed experiments can be found in the `data` folder and binarized images can be found in the `images` folder.


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

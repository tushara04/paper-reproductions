# Mechanism of branching morphogenesis inspired by diatom silica formation

This repository is my implementation of the work of **I. Babenko, N. Kröger, & B.M. Friedrich, 2024**.

## Introduction

### Paper Summary

### Reproducing What?

## Repository Structure
```
bm_friedrich_2024/
├── src/
├── data/
├── results/
├── notebooks/
└── README.md
```

## Setup 

### Requirements
To start, first set up a virtual environment in a project directory. Note that the commands that follow are run on Arch Linux but they can similarly be ran on other OSes.

```
python -m venv env 
. env/bin/activate
```

To install requirements:
```
pip install -r requirements.txt
```

### Downloading dataset
Inside the project directory, run: 
```
wget https://zenodo.org/records/8095546/files/diatom-branching-morphogenesis-v1.0.zip
unzip diatom-branching-morphogenesis-v1.0.zip 
```
for automatic install. Or, manually download the zip file and move to the directory.

### Navigating the Dataset
structured in order of files ran:
```
Folder Hierarchy:

diatom-branching-morphogenesis-v1.0
├── tem.image.analysis
│   ├── adaptive_thresholding.ipynb
│   ├── images
│   │   ├── img_001_optimized.jpg
│   │   ├── ...
│   │   └── img_038_optimized.jpg
│   ├── local_thresholding.py
│   ├── magnifications.txt
│   ├── pixel_pruning.py
│   └── __pycache__
│       ├── local_thresholding.cpython-37.pyc
│       └── pixel_pruning.cpython-37.pyc
├── t.pseudonana.model
│   ├── BranchDiatom.py
│   ├── get_valve_morphology.py
│   ├── __pycache__
│   │   ├── BranchDiatom.cpython-37.pyc
│   │   └── get_valve_morphology.cpython-37.pyc
│   ├── seed.png
│   └── simulations.ipynb
├── growing.SDV.domain
│   ├── BranchDiatom.py
│   ├── __pycache__
│   │   ├── BranchDiatom.cpython-37.pyc
│   │   └── laplacians.cpython-37.pyc
│   ├── seed_distorted.png
│   └── t.pseudonana.simulations.SDV.ipynb
├── aberrants
│   ├── laplacians.py
│   ├── seed_twos1.png
│   └── t.pseudonana.simulations.abberants.ipynb
├── a.sibiricum.model
│   ├── laplacians.py
│   ├── pennate_simulation.ipynb
│   └── __pycache__
│       └── laplacians.cpython-37.pyc
└── c.cryptica
    └── simulations.ipynb
```

## Reproducing the Results
All the outputs are saved in the results/ directory

<run a specific specifc and paste the key results and explain briefly. if any difference, i will mention that.

## Notes on Reproducibility

## Conclusion
Reflection on:
- what i learned
- what worked
- what remains if anything

## Citation
**Paper**: I. Babenko, N. Kröger, & B.M. Friedrich, Mechanism of branching morphogenesis inspired by diatom silica formation, Proc. Natl. Acad. Sci. U.S.A. 121 (10) e2309518121, https://doi.org/10.1073/pnas.2309518121 (2024).

**Dataset**: Iaroslav Babenko. (2023). Mechanism of branching morphogenesis inspired by diatom silica formation. Zenodo. https://doi.org/10.5281/zenodo.8095546

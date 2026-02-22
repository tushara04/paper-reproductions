Minimal model of the diatom branching silica morphogenesis

Iaroslav Babenko, TU Dresden
19.06.2023
iaroslav.babenko@tu-dresden.de

repository : https://doi.org/..

Synopsis:
The current version of this repository contains most essential python scripts
relative for the submitted manuscript 'Mechanism of branching morphogenesis 
inspired by diatom silica formation' (2023). The folders contain following:

I.  TEM image analysis for quantification of nascent silica pattern in diatoms
    a. Skeleton extraction from the valve SDV TEM images........(Figs. 2)
    b. Skeleton morphology quantification script................(Figs. 2)
    c. Folder containing raw TEM data
    d. Folder containing recognized skeletons
    
II. Simulations of the PDEs describing the model's kinetics that contain:
    a. T. pseudonana minimal model in an unbounded domain.........(Figs. 2, 3)
    b. T. pseudonana minimal model inside an expanding SDV....... (Figs. S5)
    c. T. pseudonana model of abnormal morphologies.............. (Figs. 4)
    d. C. cryptica model simulations with a parametric switch ....(Figs. 4)
    e. Pennate diatom simulation with specific PSS................(Figs. 4)

Some of the images used here were manually corrected using GIMP image redactor
in order to improve robustness of the skeleton recognition algorithm. 

License:
- see LICENSE.TXT (GNU public licence v3)

Used packages and their versions:

python 3.7.4 (default, Jun 06 2023, 15:35:49) [GCC 7.3.0] 
numpy_v........ 1.17.2 
imageio_v...... 2.6.0 aa
matplotlib_v... 3.1.3 
seaborn........ 0.9.0

Folder hierarchy  :
├── aberrants
│   ├── laplacians.py
│   ├── seed_twos1.png
│   └── t.pseudonana.simulations.abberants.ipynb
├── a.sibiricum.model
│   ├── laplacians.py
│   ├── pennate_simulation.ipynb
│   └── __pycache__
│       └── laplacians.cpython-37.pyc
├── c.cryptica
│   └── simulations.ipynb
├── growing.SDV.domain
│   ├── BranchDiatom.py
│   ├── __pycache__
│   │   ├── BranchDiatom.cpython-37.pyc
│   │   └── laplacians.cpython-37.pyc
│   ├── seed_distorted.png
│   └── t.pseudonana.simulations.SDV.ipynb
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
└── t.pseudonana.model
    ├── BranchDiatom.py
    ├── get_valve_morphology.py
    ├── __pycache__
    │   ├── BranchDiatom.cpython-37.pyc
    │   └── get_valve_morphology.cpython-37.pyc
    ├── seed.png
    └── simulations.ipynb



### Overview
This document attempts to describe what is needed for a typical python notebook environment with multiprocessing using MPI.

The setup consists of:
- 1 notebook server (jupyter) per user
- 1 ipcontroller
- multiple ipengines, optionally on multiple compute nodes

The ipcontroller is listening for requires from the jupyter notebook, and sends them to the ipengines.
When the calculation is done, it sends the results back to the notebook.

Typical startup sequence:

1. start the ipcontroller
2. start ipengines, that connect to the ipcontroller
3. start (or use existing) jupyter, and connect to the ipcontroller.



The main python packages considered here are:
- numpy
- scipy
- matplotlib
- healpy
- astropy
- mpi4py
- cython
- jupyter
- ipyparallel


### OS Dependencies (CentOS)
The following packages are required for building python and/or packages.
- gcc
- libpng-devel
- freetype-devel
- bzip2-devel
- openssl-devel

For compute nodes it is enough to have the runtime version of these libraries:
- libpng
- freetype
- bzip2
- openssl


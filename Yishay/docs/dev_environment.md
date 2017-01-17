### Overview
This document attempts to describe what is needed for a typical python notebook environment with multiprocessing using MPI.

The setup consists of:
- 1 notebook server (jupyter) per user
- 1 ipcontroller
- multiple ipengines, optionally on multiple compute nodes

The ipcontroller is listening for requires from the jupyter notebook, and sends them to the ipengines.
When the calculation is done, it sends the results back to the notebook.

Typical startup sequence:

1. start an `ipcontroller`
2. start `ipengine` instances (using `mpirun`), that connect to the ipcontroller
3. start a (or use an existing) `jupyter` instance, and connect to the ipcontroller.


The main python packages considered here are:
- `numpy`
- `scipy`
- `matplotlib`
- `healpy`
- `astropy`
- `mpi4py`
- `cython`
- `jupyter`
- `ipyparallel`


### OS Dependencies (CentOS)
The following packages are required for building python and/or packages.
- `gcc`
- `libpng-devel`
- `freetype-devel`
- `bzip2-devel`
- `openssl-devel`
- `sqlite-devel`
- Python (3.6)

Python3 must be compiled with support for `sqlite3` and `bzip2` for the above packages to work.
It must also be compiled with `ssl` support so that packages are installable using `pip`.

For compute nodes it is enough to have the runtime version of these libraries:
- `libpng`
- `freetype`
- `bzip2`
- `openssl`


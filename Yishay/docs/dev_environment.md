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
- `sqlite` (?)


### Initial Setup

0. Make sure all required dependencies are installed.
1. Create a new python virtual environment, for example:
  `/path/to/python -m venv $HOME/venv`
2. Activate the virtual environment for the current bash shell:
  `source ~/vent/bin/activate`
3. Install python packages:
  `pip install healpy scipy cython mpi4py jupyter ipyparallel`
  
#### IPyParallel Setup

#### PBS Integration

##### Notebook script:

* If the notebooks are going to be mostly idle, we can set `ncpus` to 0.
* Make sure to choose unique port number per user.

```bash
#!/bin/bash
#PBS -l select=1:ncpus=0
#PBS -N jupyter_notebook
#PBS -j oe

cd $PBS_O_WORKDIR
mkdir $PBS_JOBID
cat /etc/hostname |cut -f1 -d'.' > $HOME/jupyter_current_host
source $HOME/venv/bin/activate
jupyter notebook --no-browser --port=8895 2>&1 | tee $PBS_JOBID/jupyter_output
```

##### IPEngine Script

Change `select` parameters according to job requirements and available resources (see <http://wiki-hpc/index.php/Basic_information_(Astro)>).

```bash
#!/bin/bash
#PBS -l select=1:ncpus=3:mpiprocs=3:mem=1gb
#PBS -N ipengine
#PBS -j oe

cd $PBS_O_WORKDIR

#get ip address of current controller
IP_ADDR=$(cat $HOME/$CTRL_JOBID/ipcontroller_current_ip)

source $HOME/venv/bin/activate
mpirun ipengine --timeout=60.0 --mpi=mpi4py --profile=pbs --ip=$IP_ADDR
```

##### IPController Script

```bash
#!/bin/bash
#PBS -l select=1:ncpus=0
#PBS -N ipcontroller
#PBS -j oe

## save node name
## (not used at the moment)
cat /etc/hostname |cut -f1 -d'.' > $HOME/ipcontroller_current_host

## get node ethernet IP
IP_ADDR=$(ip addr show eno1 | grep '^[ ]*inet ' | cut -f6 -d' '|cut -f1 -d'/')
mkdir $HOME/$PBS_JOBID
echo $IP_ADDR > $HOME/$PBS_JOBID/ipcontroller_current_ip

cd $PBS_O_WORKDIR
source $HOME/venv/bin/activate
ipcontroller --profile=pbs --ip=$IP_ADDR
```

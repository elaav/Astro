### Quick Start Guide

0. connect to `astrophys2`  

1. Start a jupyter notebook server:  
  `qsub -q bigmem ipengine.pbs`

2. Start an ipcontroller instance:  
  `qsub -q bigmem ipcontroller.pbs`

3. Edit `ipengine.pbs` to select the desired number of cores:  
  For example, to use 24 cores write:  
  `#PBS -l select=1:ncpus=24:mpiprocs=24`

4. Start ipengine instances:  
  `qsub -q bigmem ipengine.pbs`

* note: the `-q bigmem` argument can also be added to the `pbs` scripts

5. If you do not have port forwarding for the notebook server set up by default, 
  you may create it for the current session:  
  press <kbd>Enter</kbd> followed by <kbd>Shift</kbd>+<kbd>~</kbd> and then <kbd>Shift</kbd>+<kbd>C</kbd>.

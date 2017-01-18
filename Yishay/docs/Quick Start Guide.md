### Quick Start Guide

0. connect to `astrophys2`  

1. If you do not have port forwarding for the notebook server set up by default, 
  you may create it for the current session:  
  a. press <kbd>Enter</kbd> followed by <kbd>Shift</kbd>+<kbd>~</kbd> and then <kbd>Shift</kbd>+<kbd>C</kbd>.  
  b. A special `ssh> ` prompt should appear. Type `-L <local_port>:localhost:<remote_port>`.  
     It is convenient to keep the local and remote ports the same.  
     For example:  
     `ssh> -L 8895:localhost:8895`

2. Start a jupyter notebook server:  
  `qsub -q bigmem ipengine.pbs`  
  A job ID will be displayed.
  The connection details are saved in a file. To view it type:  
  `head 1134.astrophys.local/jupyter_output` (where `1134.astrophys.local` is the job ID in this case)  
  Look for a part that looks like this:  
  ```
      Copy/paste this URL into your browser when you connect for the first time,
      to login with a token:
           http://localhost:8895/?token=0641dd2d8c91c7ce48e87111207b05872c9cccba6967fb24
  ```  
  Open the link in your browser to access the jupyter notebook.

3. Start an ipcontroller instance:  
  `qsub -q bigmem ipcontroller.pbs`

4. Edit `ipengine.pbs` to select the desired number of processes:  
  For example, to use 24 processes write:  
  `#PBS -l select=1:ncpus=24:mpiprocs=24`

5. Start ipengine instances:  
  `qsub -q bigmem ipengine.pbs`

  * note: the `-q bigmem` argument can also be added to the `pbs` scripts

6. You may use the following script to make sure that everything is working:  
   ```python
   from ipyparallel import Client
   c = Client(profile='pbs')
   print(len(c))
   ```

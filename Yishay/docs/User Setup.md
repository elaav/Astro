### User Setup

0. (Optional) Set up port forwarding for jupyter notebooks:  
  1. Edit the `ssh` configuration file on your local computer:  
     ```vi ~/.ssh/config```  
  2. Add the following:
  ```
  Host astrophys2
  HostName astrophys2.tau.ac.il
  User <TAU_user_name>
  ProxyCommand ssh <TAU_user_name>@gate.tau.ac.il -W %h:%p
  LocalForward localhost:8895 localhost:8895
   ```  
   * The `ProxyCommand` line is not needed on a university desktop computer on a wired network.
   * Change `<TAU_user_name>` to your actual username.

1. Connect to `astrophys2`

2. Obtain the following scripts (location TBD):
  * `ipcontroller.pbs`
  * `ipengine.pbs`
  * `jupyter.pbs`  
  Put the files in your home directory.

3. Create a python virtual environment:  
  `/path/to/python36/bin/python3.6 -m venv ~/venv`

4. Activate the virtual environment for the current bash shell:  
  `source ~/vent/bin/activate`

5. Install python packages:  
  `pip install healpy scipy cython mpi4py jupyter ipyparallel`


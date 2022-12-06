Prerequisites
-------------
* Python 3.x
* Set up Kaggle authentication: on your Kaggle account, under API, select `Create New API Token`, and a `kaggle.json` file will be downloaded on your computer. Move this file to `~/.kaggle/kaggle.json` on MacOS/Linux. Remember to run `chmod 600 ~/.kaggle/kaggle.json` to ensure it is only readable for you.
* Mac OSX users: Run `brew install libomp` to install OpenMP runtime (for Xboost). This step requires that homebrew has been installed.

Get started
------------

     # install virtualenv
     pip3 install virtualenv
     
     # create a virtual environment
     virtualenv venv --python=<path-to-python-3.*>  # the version used: 3.11.0
     
     # activate environment
     source venv/bin/activate
     
     # install requirements
     pip3 install -r requirements.txt
     
     # set the global environment variables
     source global_env.sh
     
     # install local python packages
     python3 setup.py install
     pip3 install -e .



Notebooks
---------
Install ipykernel in your activated virtual environment (provides Ipython kernel for Jupyter)

		pip3 install ipykernel

Add the kernel to jupyter notebook

		python3 -m ipykernel install --user --name=<project_env_name>
    
When done, deactivate the environment

		deactivate

Add the virtual environment in the jupyter notebook: in your python notebook --> kernel --> change kernel --> <project_env_name>

**How to remove a virtual environment from Jupyter**

Remove the virtual directory

		rm -rf <project_env_name>

Check the list of environments added to Jupyter notebook
		
		jupyter kernelspec list

Remove the environment
	
	jupyter kernelspec uninstall <project_env_name>

    
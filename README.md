Prerequisites
-------------
* Python 3.8
* Java8 or higher

Setting up the environment for this project
-------------------------------------------

1. If not already installed, install virtualenv:

         pip install virtualenv

2. Create a virtual environment with Python 3.8 using virtualenv:

         virtualenv venv --python=3.8

3. Activate the virtual environment and install dependencies from the requirements.txt file and local python packages:

         source venv/bin/activate
         pip install -r requirements.txt
         pip install -e .

Set up virtual environment kernel for Jupyter Notebook
------------------------------------------------------
If not already installed, install ipykernel in your activated virtual environment (provides Ipython kernel for Jupyter)

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

Setting up PySpark and Jupyter Notebook
---------------------------------------
1. Download the latest prebuilt package of [Spark](https://spark.apache.org/downloads.html) for Hadoop.
   

2. Untar the  Spark tgz file and move it to the `/opt/` directory and create a symbolic link (this allows you to download and use multiple Spark versions.):
       
        tar -xzf spark-<version>-bin-hadoop<version>.tgz
        mv spark-<version>-bin-hadoop<version> /opt/spark-<version>
        ln -s /opt/spark-<version> /opt/spark̀

3. Install `PySpark` and `Jupyter`:
        
        pip install pyspark
        pip install jupyter

4. Configure the `$PATH` variables by adding the following lines in your `~/.bash_profile`, `~/.bashrc` or `~/.zshrc`:
        
        # Locate Spark
        export SPARK_HOME=/opt/spark
        export PATH=$SPARK_HOME/bin:$PATH
   
        # Set up PySpark Jupyter Notebook diver
        export PYSPARK_DRIVER_PYTHON=jupyter
        export PYSPARK_DRIVER_PYTHON_OPTS='notebook'

5. Restart your terminal (or `source <PATH file>`) and enter `pyspark` to get started.

**NOTE**: The `$PATH` variables has been added to the global_env.sh file (i.e., `source global_env.sh`)

Run executables
---------------
Fetch and clean PubMed abstracts (query: `diabetes`, change in `global_env.sh` if another topic is of your interest)

      sh $FETCH_AND_CLEAN

Repository overview
---------------
      .
      ├── README.md                           # README file
      ├── data                                # Data directory
      │     ├── proc                            # Processed data
      │     ├── raw                             # Raw data
      │   └── results                         # Results or derived/summary data
      ├── exec                                # Executables
      │   └── fetch_and_clean_abstracts.sh    # Executable for abstract fetching and cleaning
      ├── global_env.sh                       # Global environment variables
      ├── requirements.txt                    # Environment dependencies
      ├── setup.py                            # Setup script to install local modules
      └── src                                 # Source code
          ├── __init__.py                     # __init__ file to create Python package
          ├── fetch_abstracts.py              # Python script for fetching PubMed abstracts
          ├── preprocess_abstracts.py         # Python scrip for preprocessing and cleaning PubMed abstracts
          └── pubmed_countries.py             # Country dictionary for country standardisation

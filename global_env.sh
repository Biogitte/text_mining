#!/bin/bash

# Working directory - remember to specify accordingly.
export WORK_DIR=$PWD

# Setting up Spark
export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$PATH
# Setting up PySpark Jupyter Notebook driver
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'

# Data directories
mkdir -p $WORK_DIR/data
export DATA=$WORK_DIR/data
mkdir -p $DATA/raw
export DATA_RAW=$DATA/raw
mkdir -p $DATA/proc
export DATA_PROC=$DATA/proc
mkdir -p $DATA/results
export DATA_RESULTS=$DATA/results

# Source code directory
export SRC=$WORK_DIR/src

# Executables
export EXEC=$WORK_DIR/exec

# Jupyter Notebooks directory
export NOTEBOOKS=$WORK_DIR/notebooks

# Variables related to fetching PubMed abstracts
export FETCH_ABSTRACTS=$SRC/fetch_abstracts.py
export EMAIl='TODO@TODO.dk'
export QUERY='diabetes'

# Variables related to data cleaning and preparation of PubMed abstracts
export CLEAN_ABSTRACTS=$SRC/clean_abstracts.py

# Executables to fetch and clean abstracts
export FETCH_AND_CLEAN=$EXEC/fetch_and_clean_abstracts.sh
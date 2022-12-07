#!/bin/bash

# Working directory - remember to specify accordingly.
export WORK_DIR=$PWD

# Data directories
export DATA=$WORK_DIR/data
export DATA_RAW=$DATA/raw
export DATA_PROC=$DATA/processed

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
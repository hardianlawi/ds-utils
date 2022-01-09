#!/bin/bash

PROJECT_NAME = ""

conda create -f -n ${PROJECT_NAME} python=3.8 conda

_PYTHON = ${CONDA_PREFIX}/envs/${PROJECT_NAME}/bin/python
_PIP = ${CONDA_PREFIX}/envs/${PROJECT_NAME}/bin/pip

${_PIP} install seaborn
${_PIP} install pandas
${_PIP} install numpy
${_PIP} install torch
${_PIP} install ipython
${_PIP} install ipykernel

${_PYTHON} -m ipykernel install --user --name ${PROJECT_NAME}
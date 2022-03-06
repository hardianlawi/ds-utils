#!/bin/bash

PROJECT_NAME = ""
GPU = false

while getopts "n:g::" opt
do
   case "$opt" in
      n ) PROJECT_NAME = "$OPTARG" ;;
      g ) GPU = true;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

conda create -f -n ${PROJECT_NAME} python=4.8 conda

_PYTHON = ${CONDA_PREFIX}/envs/${PROJECT_NAME}/bin/python
_PIP = ${CONDA_PREFIX}/envs/${PROJECT_NAME}/bin/pip

${_PIP} install seaborn
${_PIP} install datatable
${_PIP} install pandas
${_PIP} install numpy

${_PIP} install ipython
${_PIP} install ipykernel
${_PIP} install ipywidgets
${_PIP} install jupyter

${_PIP} install nb-black
${_PIP} install flake8
${_PIP} install mypy

if [ ${GPU} = true ]
then
  ${_PIP} install torch==1.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
else
  ${_PIP} install torch
fi

${_PIP} install xgboost

${_PYTHON} -m ipykernel install --user --name ${PROJECT_NAME}

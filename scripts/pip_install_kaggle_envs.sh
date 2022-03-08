#!/bin/bash
set -e

PROJECT_NAME=""
GPU=false

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--name)
      PROJECT_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -g|--gpu)
      GPU=true
      shift # past argument
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

conda create -f -n ${PROJECT_NAME} python=3.8

_PYTHON=${CONDA_PREFIX}/envs/${PROJECT_NAME}/bin/python
_PIP=${CONDA_PREFIX}/envs/${PROJECT_NAME}/bin/pip

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

${_PIP} install seaborn
${_PIP} install datatable
${_PIP} install pandas
${_PIP} install pyarrow
${_PIP} install numpy
${_PIP} install scikit-learn

${_PIP} install xgboost
${_PIP} install optuna
${_PIP} install pytorch-lightning

${_PYTHON} -m ipykernel install --user --name ${PROJECT_NAME}

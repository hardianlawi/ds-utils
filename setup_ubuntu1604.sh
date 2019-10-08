sudo locale-gen en_SG.UTF-8

# Update and Upgrade
sudo apt update && sudo apt upgrade

# Install Docker
curl https://get.docker.com | bash

# SUGGESTED CuDA and CUDNN Version
# CuDA: 9.0.x
# CuDNN: 7.0.x

# Install Anaconda (https://www.anaconda.com/distribution/)
wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
bash Anaconda3-5.1.0-Linux-x86_64.sh

# Install packages
sudo apt install gcc htop make

# Install Nvidia Driver
# http://www.nvidia.com/Download/index.aspx?lang=en-us

# For Tesla P100
wget http://us.download.nvidia.com/tesla/390.30/nvidia-diag-driver-local-repo-ubuntu1604-390.30_1.0-1_amd64.deb
sudo dpkg -i nvidia-diag-driver-local-repo-ubuntu1604-390.30_1.0-1_amd64.deb
sudo apt-key add /var/nvidia-diag-driver-local-repo-390.30/7fa2af80.pub

# Install Cuda
# Guide: http://docs.nvidia.com/cuda/cuda-installation-guide-linux
# http://developer.nvidia.com/cuda-downloads

# Cuda-9.1
# wget https://developer.nvidia.com/compute/cuda/9.1/Prod/local_installers/cuda-repo-ubuntu1604-9-1-local_9.1.85-1_amd64
# sudo dpkg -i cuda-repo-ubuntu1604-9-1-local_9.1.85-1_amd64
# sudo apt-key add /var/cuda-repo-9-1-local/7fa2af80.pub
# sudo apt update && sudo apt upgrade
# sudo apt install cuda
# export PATH=/usr/local/cuda-9.1/bin${PATH:+:${PATH}}
# export LD_LIBRARY_PATH=/usr/local/cuda-9.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
# echo 'export PATH=/usr/local/cuda-9.1/bin${PATH:+:${PATH}}' >> .bashrc
# echo 'export LD_LIBRARY_PATH=/usr/local/cuda-9.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> .bashrc

# Cuda-9.0
wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64-deb
sudo dpkg -i cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64-deb
sudo apt update && sudo apt upgrade
sudo apt install cuda
export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
echo 'export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}' >> .bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> .bashrc

# Nvidia Toolkit
sudo apt install nvidia-cuda-toolkit

# Install CudNN
# Guide: http://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html
# https://developer.nvidia.com/rdp/cudnn-download
#
# Download: 
# cuDNN Runtime Library for Ubuntu16.04 (Deb)
# cuDNN Developer Library for Ubuntu16.04 (Deb)
# cuDNN Code Samples and User Guide for Ubuntu16.04 (Deb)

# Download the Debian packages and run
sudo dpkg -i libcudnn7*

# sudo vim /usr/include/cudnn.h
# change `#include "driver_types.h"` to `#include <driver_types.h>`

# Test CudNN installation
cp -r /usr/src/cudnn_samples_v7/ $HOME
cd  $HOME/cudnn_samples_v7/mnistCUDNN
make clean && make
./mnistCUDNN

# Update Conda
conda update -n base conda

# Create conda environment
conda create -n tensorflow pip python=3.6.4

# Activate tensorflow environment
source activate tensorflow

# GPU support
pip install --ignore-installed --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.12.0-cp36-cp36m-linux_x86_64.whl

# CPU support
pip install --ignore-installed --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.8.0-cp36-cp36m-linux_x86_64.whl
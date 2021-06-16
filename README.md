# CUDA and cuDNN Installation

1. Verify if you have CUDA-capable GPU by running `lspci | grep -i nvidia`
2. Run `sudo apt install gcc`
3. Install CUDA by simply heading to [this link](http://developer.nvidia.com/cuda-downloads) and copy paste the commands provided.
4. Run `sudo apt install nvidia-cuda-toolkit`
5. Install cuDNN by following the steps below
   1. Head to [this link](https://developer.nvidia.com/rdp/cudnn-download).
   2. Create an account and download the cuDNN files that are compatible with the CUDA installed in the previous step. To check the installed version, run `nvcc -V`. This only works after installing the cuda toolkit.
      - cuDNN Runtime Library
      - cuDNN Developer Library
      - cuDNN Code Samples and User Guide
    3. (Optional) Installed files will go to your local machine. If you are using a Virtual Machine, you can transfer those files by running `scp -i <path to private key> ~/Downloads/libcudnn* username@host:/home/user/`.
    4. Head to [this link](https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#installlinux-deb) and follow the installation instruction.

> The steps are specifically for Ubuntu/Debian users.

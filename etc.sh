# scp
scp /local/directory username@from_host:file.txt

# Update all expired keys from Ubuntu key server in one command:
# From https://stackoverflow.com/questions/34733340/mongodb-gpg-invalid-signatures
sudo apt-key list | \
 grep "expired: " | \
 sed -ne 's|pub .*/\([^ ]*\) .*|\1|gp' | \
 xargs -n1 sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys

# Kill a list of processes
sudo kill -9 $(ps aux | grep <process> | awk '{print $2}')

# Pretty print JSON in Bash
# Need to install jq by running `apt-get install jq`
curl -X POST -d @filename.json http://localhost:8080/api/v1/load_test | jq .

### Install new python environment Conda ###
conda create -n yourenvname python=x.x anaconda
conda activate yourenvname
conda remove -n yourenvname --all

# Useful Add-ons for Jupyter Notebooks
# https://github.com/dunovank/jupyter-themes
# https://towardsdatascience.com/bringing-the-best-out-of-jupyter-notebooks-for-data-science-f0871519ca29
pip install jupyter_contrib_nbextensions && jupyter contrib nbextension install --user
pip install ipywidgets && jupyter nbextension enable --py widgetsnbextension
pip install jupyterthemes
# dark
jt -t onedork -fs 95 -altp -tfs 11 -nfs 115 -cellw 88% -kl -N
# light
jt -t grade3 -fs 95 -altp -tfs 11 -nfs 115 -cellw 88% -kl -N

### Install python kernel in Jupyter Notebook ###
pip install ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"

# Remove kernel from jupyter
jupyter kernelspec uninstall unwanted-kernel
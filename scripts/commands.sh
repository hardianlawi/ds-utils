# Change all file extensions to lowercase/uppercase
zmv '(*).(*)' '$1.$2:l'
zmv '(*).(*)' '$1.$2:u'

# Wipe all whitespace including newlines
cat file.txt | tr -d " \t\n\r"

# Get machine IP
hostname -I | awk 'print $1'

# Store keygen
ssh-add .ssh/google_compute_engine

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

# Remove pycache files
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

# Remove (base) prefix from terminal
conda config --set changeps1 False

### Install new python environment Conda ###
conda create -n yourenvname python=x.x conda
conda env create -f environment.yml
conda activate yourenvname
conda remove -n yourenvname --all

# Export conda environment
conda env export > environment.yml
conda env export --no-builds > environment.yml
conda env export --no-builds | grep -v "prefix" > environment.yml

# Create new python environment
conda env create -f environment.yml
conda create -n <environment-name> --file req.txt

# Change default shell to zsh
sudo sed s/required/sufficient/g -i /etc/pam.d/chsh
chsh -s $(which zsh)

# Port forward
# https://ljvmiranda921.github.io/notebook/2018/01/31/running-a-jupyter-notebook/
# -N: suppresses the execution of a remote command. Pretty much used in port forwarding.
# -f: this requests the ssh command to go to background before execution.
# -L: this argument requires an input in the form of local_socket:remote_socket.
# Here, we’re specifying our port as YYYY which will be binded to the port XXXX
# from your remote connection.
ssh -N -f -L localhost:<your machine port>:localhost:<remote machine port> user@ip_address -i <private key path>

# Untar file
tar -xvzf <FILE_PATH>

#####################
# Jupyter Notebooks #
#####################

# Useful Add-ons for Jupyter Notebooks
# https://github.com/dunovank/jupyter-themes
# https://towardsdatascience.com/bringing-the-best-out-of-jupyter-notebooks-for-data-science-f0871519ca29
pip install jupyter_contrib_nbextensions && jupyter contrib nbextension install --user
pip install ipywidgets && jupyter nbextension enable --py widgetsnbextension
pip install jupyterthemes
# dark
# jt -t onedork -fs 95 -altp -tfs 11 -nfs 115 -cellw 88% -kl -N
# light
# jt -t grade3 -fs 95 -altp -tfs 11 -nfs 115 -cellw 88% -kl -N
jt -t grade3 -fs 95 -tfs 11 -nfs 115 -cellw 88% -kl -N -T

### Install python kernel in Jupyter Notebook ###
# pip install ipykernel
# pip install black
# pip install nb-black
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
poetry run ipython kernel install --user --name myenv --display-name "Python (myenv)"

# Remove kernel from jupyter
jupyter kernelspec list
jupyter kernelspec uninstall unwanted-kernel

#########################
# Google Cloud Platform #
#########################

gcloud config set account ${EMAIL}
gcloud auth application-default login

# Formatting and mounting persistent disk to VM (https://cloud.google.com/compute/docs/disks/add-persistent-disk)
sudo mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/[DEVICE_ID]
sudo mkdir -p /mnt/disks/[MNT_DIR]
sudo mount -o discard,defaults /dev/[DEVICE_ID] /mnt/disks/[MNT_DIR]
sudo chmod a+w /mnt/disks/[MNT_DIR]

# Print ip address
hostname --ip-address

# Copy data from production to staging
bq query \
  --use_legacy_sql=false \
  --destination_table="$BQ_DATASET.$table" \
  --project_id="gods-staging" \
  --display_name="cp $BQ_DATASET.$table to gods-staging" \
  --schedule="every 24 hours" \
  --append_table \
    "SELECT * from \`gods-production.$BQ_DATASET.$table\` WHERE DATE(event_timestamp)=DATE_SUB(@run_date, INTERVAL 1 DAY)"


#################
#      Tmux     #
#################

# start new with session name
tmux new -s myname

# attach
tmux a -t myname

# list sessions
tmux ls

# kill session
tmux kill-session -t myname

# detach
# Ctrl b + d

#################
#     Redis     #
#################

# Install Redis
sudo apt install make gcc tcl
curl -s -o redis-stable.tar.gz http://download.redis.io/redis-stable.tar.gz
tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd /usr/local/lib/redis-stable/
make && make install
cd


####################
#       Git        #
####################

# Reset files from staging
git checkout HEAD -- <files>

# Undo a public commit with git revert
git revert <SHA_ID>

# Undo a commit with git reset
git reset --hard <SHA_ID>

# Undoing the last commit
git add .
git commit --amend -m""

# Archive git repository as zip file
git archive --format zip --output /full/path/to/zipfile.zip master

# Rebase
git rebase <branch name to be rebased on>
git rebase --continue
git rebase --abort

# Cherry pick
git cherry-pick <SHA_ID>

# Worktree
git worktree add <DIR> -b <BRANCH_NAME>

####################
#      docker      #
####################

# Install docker
curl https://get.docker.com | bash

# https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket
sudo groupadd docker
sudo usermod -aG docker $USER
docker run hello-world

# Build image
docker build -t <tag name> .
docker build --build-arg SOME_ENV_VAR=hello -t <tag name> -f Dockerfile .

# Check list of images
docker images

# Run docker
# -it attaches to an interactive tty in the container -it <Image name> sh
# --rm automatically removes the container when it exits
docker run

# https://stackoverflow.com/questions/30209776/docker-container-will-automatically-stop-after-docker-run-d
docker run -d <image> sleep infinity
docker run -t -d <image> 


# shows all containers that are currently running
docker ps

# Delete all exited containers
docker rm $(docker ps -a -q -f status=exited)
# or
docker container prune

# Delete image
docker rmi

# Delete all images (Clean up)
docker rmi -f $(docker images -a -q)
docker system prune -a -f
docker volume rm $(docker volume ls -qf dangling=true)

# Print all the logs
docker logs -f <CONTAINER ID>

# SSH into a running container
docker exec -it <CONTAINER ID> /bin/bash
# or more generally
docker exec -it <CONTAINER ID> <command>

# Starting an app
docker container run --publish 8000:8080 --detach bulletinboard:1.0

# Stop application
docker stop <CONTAINER ID>

# Start multiple containers
docker compose up -d
docker compose down # Stop multiple containers


##########
# Golang #
##########

# Clean dependencies
go clean -cache -modcache -i -r

# Download latest version of dependencies to $GOPATH
# This would add/remove dependencies used inside go files to go.mod
go get ./...

# Download dependencies listed in go.mod
go mod download
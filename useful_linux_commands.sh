### Install new python environment Conda ###
conda create -n yourenvname python=x.x anaconda
source activate yourenvname
conda remove -n yourenvname --all

### Install python kernel in Jupyter Notebook ###
pip install ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"

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


#########################
# Basic Docker Commands #
#########################

# Install docker
curl https://get.docker.com | bash

# Build image
docker build -t <tag name> .

# Run docker
# -it attaches to an interactive tty in the container -it <Image name> sh
# --rm automatically removes the container when it exits
docker run

# shows all containers that are currently running
docker ps

# Delete all exited containers
docker rm $(docker ps -a -q -f status=exited)
# or
docker container prune

# Delete image
docker rmi

#########
# Redis #
#########

curl -s -o redis-stable.tar.gz http://download.redis.io/redis-stable.tar.gz
tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd /usr/local/lib/redis-stable/
make && make install
cd

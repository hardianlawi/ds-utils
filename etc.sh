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
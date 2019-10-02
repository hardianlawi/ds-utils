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

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
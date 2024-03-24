#!/usr/bin/env zsh

# Define variables
IMAGE_NAME="flask_app"
CONTAINER_NAME="JobApplicationManager"
PORTNUMBER=5001

# Step 1: Stop the Docker container if it is running
if docker ps | grep -q $CONTAINER_NAME; then
    echo "Stopping container $CONTAINER_NAME..."
    docker stop $CONTAINER_NAME
fi

# Step 2: Remove the Docker container if it exists
if docker ps -a | grep -q $CONTAINER_NAME; then
    echo "Removing container $CONTAINER_NAME..."
    docker rm $CONTAINER_NAME
fi

# Step 3: Remove the Docker image if it exists
if docker images | grep -q $IMAGE_NAME; then
    echo "Removing image $IMAGE_NAME..."
    docker rmi $IMAGE_NAME
fi

# Step 4: Build a new Docker image from Dockerfile
echo "Building new image $IMAGE_NAME ..."
docker build -t $IMAGE_NAME .

# Step 5: Run a container from the new Docker image
echo "Running new container $CONTAINER_NAME from image $IMAGE_NAME: ..."
docker run --name $CONTAINER_NAME -p $PORTNUMBER:$PORTNUMBER $IMAGE_NAME

# End of script
echo "Script completed."
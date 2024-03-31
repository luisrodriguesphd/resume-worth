#!/bin/bash

# Navigate to the directory containing the Dockerfile
cd .

# Build the Docker image
docker build -t resume-worth:latest . --build-arg REQUIREMENTS_PATH="./requirements.in"

# Check if the image was created successfully
docker images | grep resume-worth

# Run docker image
# docker run -it -p 7860:7860 resume-worth
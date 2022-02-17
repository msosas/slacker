#!/bin/bash

IMAGE_NAME="slacker"

sudo docker build -t $IMAGE_NAME .
sudo docker save -o ./binaries/slacker.tar $IMAGE_NAME
sudo chown -R $USER:$USER ./binaries
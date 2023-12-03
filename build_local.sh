#!/bin/bash

sudo docker buildx create --use
sudo docker buildx build --platform linux/386,linux/amd64,linux/arm/v6,linux/arm/v7,linux/arm64/v8,linux/ppc64le -t akiteck/alpine_storebox:0.1 . --push
sudo docker buildx rm
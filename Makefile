.PHONY: build format

# Variables
IMAGE_NAME = photo-slider
PLATFORM = linux/amd64
SSH_COMMAND = ssh -i ~/Downloads/PhotoSlider.pem ec2-user@ec2-16-170-253-227.eu-north-1.compute.amazonaws.com

# Build the Docker image
build:
	docker build --platform $(PLATFORM) -t $(IMAGE_NAME) .

format:
	pdm run ruff format
	pdm run ruff check --fix

push:
	docker save $(IMAGE_NAME) | $(SSH_COMMAND) docker load
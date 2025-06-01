.PHONY: build format

# Variables
IMAGE_NAME = photo-slider

# Build the Docker image
build:
    docker build -t $(IMAGE_NAME) .

format:
    pdm run ruff format
    pdm run ruff check --fix

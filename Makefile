.PHONY: build lint push up down

# Variables
IMAGE_NAME = photo-slider
PLATFORM = linux/amd64
USER = ec2-user
HOST = ec2-16-170-253-227.eu-north-1.compute.amazonaws.com
REMOTE_DIR = /home/$(USER)/photo-slider
PEM_FILE = ~/Downloads/PhotoSlider.pem
SSH_COMMAND = ssh -i $(PEM_FILE) $(USER)@$(HOST)

build:
	docker build --platform $(PLATFORM) -t $(IMAGE_NAME) .

lint:
	pdm run ruff format
	pdm run ruff check --fix

push:
	# Create remote directory
	$(SSH_COMMAND) "mkdir -p $(REMOTE_DIR)"
	# Copy necessary files excluding hidden files
	rsync -av --exclude='.*' -e "ssh -i $(PEM_FILE)" Dockerfile docker-compose.yaml pyproject.toml pdm.lock src $(USER)@$(HOST):$(REMOTE_DIR)
	# Build on remote machine
	$(SSH_COMMAND) "cd $(REMOTE_DIR) && docker build -t $(IMAGE_NAME) ."

up:
	$(SSH_COMMAND) "cd $(REMOTE_DIR) && docker-compose up -d"

down:
	$(SSH_COMMAND) "cd $(REMOTE_DIR) && docker-compose down"

.PHONY: lint push up down

# Variables
IMAGE_NAME = photo-slider
USER = ec2-user
HOST = loopslide.xyz
REMOTE_DIR = /home/$(USER)/photo-slider
PEM_FILE = ~/Downloads/PhotoSlider.pem
SSH_COMMAND = ssh -i $(PEM_FILE) $(USER)@$(HOST)

lint:
	pdm run ruff format
	pdm run ruff check --fix

push:
	# Create remote directory
	$(SSH_COMMAND) "mkdir -p $(REMOTE_DIR)"
	# Copy necessary files excluding hidden files
	rsync -av --exclude='.*' -e "ssh -i $(PEM_FILE)" Dockerfile nginx.conf docker-compose.yaml pyproject.toml pdm.lock src $(USER)@$(HOST):$(REMOTE_DIR)
	# Build on remote machine
	$(SSH_COMMAND) "cd $(REMOTE_DIR) && docker build -t $(IMAGE_NAME) ."

up:
	$(SSH_COMMAND) "cd $(REMOTE_DIR) && docker-compose up -d"

down:
	$(SSH_COMMAND) "cd $(REMOTE_DIR) && docker-compose down"

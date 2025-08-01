# Photo-Slider

### Prerequisites

- Python 3.12 is required as specified in the `pyproject.toml`.
- Ensure you have PDM installed. If not, you can install it via pip:
  ```bash
  curl -sSL https://pdm-project.org/install-pdm.py | python3 -
  ```
- Docker and Docker compose:
  ```bash
  sudo yum update
  sudo yum install docker -y
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  # Now log out, log back in and test docker
  docker ps

  sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  docker-compose version
  ```
- rclone and fuse3
  ```bash
  sudo yum install fuse3

  sudo -v ; curl https://rclone.org/install.sh | sudo bash
  rclone version
  rclone config  # At this stage configure the s3 bucket..

  mkdir -p ~/mnt/srv
  # Make sure user_allow_other is enabled in /etc/fuse.conf
  rclone mount s3:/ ~/mnt/srv/ --allow-other --vfs-cache-mode writes --daemon
  ```

## Installation Steps
### Push and run

   ```bash
   make push
   make up
   ```

### Stopping

   ```bash
   make down
   ```

### Generating SSL Certificates with Certbot

To secure your application with SSL, you can generate certificates using Certbot. Follow these steps to generate certificates for your domain:

1. **Install Certbot**: If Certbot is not already installed on your system, you can install it using your package manager. For example, on Ubuntu, you can run:

   ```bash
   sudo yum update
   sudo yum install certbot
   ```

2. **Generate Certificates**: Use Certbot to generate certificates for your domain. Replace `loopslide.xyz` and `*.loopslide.xyz` with your actual domain names:

   ```bash
   sudo certbot certonly --manual --preferred-challenges dns -d loopslide.xyz -d *.loopslide.xyz
   ```

   - This command will guide you through the process of creating DNS TXT records for domain validation. Follow the instructions provided by Certbot to complete the process.

3. **Renewal**: Certbot certificates are valid for 90 days. To renew re-run the previous steps

By following these steps, you will have SSL certificates generated for your domain, ensuring secure communication for your application.

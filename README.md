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

## SSL Certificate Configuration

Photo-Slider supports HTTPS with two SSL certificate options. Choose the option that best fits your needs:

### Option 1: Self-Signed Certificates (Development/Testing)

**Best for:** Development, testing, internal networks, or when you don't have a domain.

**Pros:**
- ✅ Quick setup (no domain validation required)
- ✅ Works offline/locally
- ✅ Free
- ✅ Good for development and testing

**Cons:**
- ⚠️ Browser security warnings
- ⚠️ Not trusted by default
- ⚠️ Not suitable for production

**Setup:**

1. **Generate certificates:**
   ```bash
   ./generate-certs.sh
   ```

2. **Start services:**
   ```bash
   docker-compose up -d
   ```

The self-signed certificates include Subject Alternative Names (SAN) for:
- `loopslide.xyz`
- `*.loopslide.xyz` (wildcard)
- `view.loopslide.xyz`
- `upload.loopslide.xyz`
- `localhost`

### Option 2: Let's Encrypt Certificates (Production)

**Best for:** Production environments with a valid domain.

**Pros:**
- ✅ Trusted by all browsers (no warnings)
- ✅ Free
- ✅ Automatic validation
- ✅ Professional appearance (green lock)

**Cons:**
- ⚠️ Requires domain ownership
- ⚠️ Need internet access for validation
- ⚠️ 90-day expiration (requires renewal)

**Setup:**

1. **Install Certbot:**
   ```bash
   sudo yum update
   sudo yum install certbot
   ```

2. **Generate certificates:**
   ```bash
   sudo certbot certonly --manual --preferred-challenges dns -d loopslide.xyz -d *.loopslide.xyz
   ```

   This will guide you through creating DNS TXT records for domain validation.

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

**Certificate locations:**
- Certificate: `/etc/letsencrypt/live/loopslide.xyz/fullchain.pem`
- Private key: `/etc/letsencrypt/live/loopslide.xyz/privkey.pem`

**Renewal:**
Certificates expire every 90 days. To renew:
```bash
sudo certbot renew
docker-compose restart nginx
```

### Current Configuration

The docker-compose.yaml is currently configured for **Let's Encrypt certificates**. To switch to self-signed certificates, you would need to:

1. Update the volume mounts in `docker-compose.yaml`
2. Update the certificate paths in `nginx.conf`

Both certificate types provide full SSL encryption - the main difference is browser trust and validation requirements.

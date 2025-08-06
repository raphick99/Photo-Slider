#!/bin/bash

# Script to generate self-signed SSL certificates for Photo-Slider

echo "Generating self-signed SSL certificates..."

# Create certificates directory
mkdir -p ./certs

# Generate private key
openssl genrsa -out ./certs/server.key 2048

# Generate certificate signing request
openssl req -new -key ./certs/server.key -out ./certs/server.csr -config <(
cat <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=US
ST=State
L=City
O=Organization
OU=OrgUnit
CN=loopslide.xyz

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = loopslide.xyz
DNS.2 = *.loopslide.xyz
DNS.3 = view.loopslide.xyz
DNS.4 = upload.loopslide.xyz
DNS.5 = localhost
IP.1 = 127.0.0.1
EOF
)

# Generate self-signed certificate
openssl x509 -req -in ./certs/server.csr -signkey ./certs/server.key -out ./certs/server.crt -days 365 -extensions v3_req -extfile <(
cat <<EOF
[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = loopslide.xyz
DNS.2 = *.loopslide.xyz
DNS.3 = view.loopslide.xyz
DNS.4 = upload.loopslide.xyz
DNS.5 = localhost
IP.1 = 127.0.0.1
EOF
)

# Set appropriate permissions
chmod 600 ./certs/server.key
chmod 644 ./certs/server.crt

# Clean up CSR file
rm ./certs/server.csr

echo "SSL certificates generated successfully!"
echo "Certificate: ./certs/server.crt"
echo "Private Key: ./certs/server.key"
echo ""
echo "Note: These are self-signed certificates. Your browser will show a security warning."
echo "For production use, consider using Let's Encrypt or purchasing a real certificate."
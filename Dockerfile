# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install PDM
RUN pip install -U pdm

# Copy PDM files
COPY pyproject.toml pdm.lock ./

# Install dependencies
RUN pdm install

# Copy source code
COPY src/ ./src/

# Run the application
CMD ["pdm", "run", "python", "src/main.py"]

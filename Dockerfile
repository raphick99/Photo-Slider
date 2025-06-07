# Use Python 3.12 as the base image
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

RUN pip install -U pdm

COPY pyproject.toml pdm.lock ./

RUN pdm install --no-editable

FROM python:3.12-slim

COPY --from=builder /app/.venv/ /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src/

CMD ["python", "/app/src/main.py"]

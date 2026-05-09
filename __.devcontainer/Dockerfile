FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates build-essential \
    pandoc \
    nodejs npm \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

RUN npm install -g @mermaid-js/mermaid-cli || true

WORKDIR /workspaces/bookMaker

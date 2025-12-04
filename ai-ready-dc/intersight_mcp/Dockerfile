FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install venv package if missing (usually included, but just in case)
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv .venv

# Upgrade pip inside venv
RUN .venv/bin/pip install --upgrade pip

# Install required packages inside venv
RUN .venv/bin/pip install mcpo==0.0.17 uv requests httpx

# Copy app source code last (to leverage Docker cache)
RUN pip install mcpo==0.0.17 uv requests

COPY . .

RUN uv add "mcp[cli]" httpx requests

RUN uv sync

# Expose port 8000 for OpenShift routing
EXPOSE 8000

CMD ["uv", "run", "intersight_api.py", "--log-level", "DEBUG"]

# Uncomment for Open WebUI MCP integration.
# CMD ["uvx", "mcpo", "--host", "0.0.0.0", "--port", "8000", "--", "uv", "run", "intersight_api.py"]
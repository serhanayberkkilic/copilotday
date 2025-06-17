FROM python:3.13-slim-bookworm

# Install curl, certificates and venv support, then clean up apt lists
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      python3-venv \
 && rm -rf /var/lib/apt/lists/*

# Download and install UV
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Make sure uv is on PATH
ENV PATH="/root/.local/bin/:$PATH"

# Copy the entire project into the image
ADD . /app
WORKDIR /app

# Create the .venv for the project
RUN uv venv

# Install all dependencies into that venv (using your uv.lock)
RUN uv sync --frozen

EXPOSE 8000

# Start the MCP server exactly as in your desktop config
CMD ["uv", "run", "--with", "mcp[cli]", "mcp", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first
COPY pyproject.toml .

# Install dependencies using uv with --system flag
RUN uv pip install --system --no-cache-dir -e .

# Copy source code and configuration
COPY src/ src/

# Environment variables
ENV GITLAB_URL=https://gitlab.com
ENV GITLAB_TOKEN=""

# Run the server
CMD ["fastmcp", "run", "src/gitlab_mcp_server/server.py:mcp"]
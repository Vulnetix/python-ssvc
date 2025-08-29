# Use a base image with package manager for development tools
FROM alpine:3.18 as tool-builder

# Install system dependencies
RUN apk add --no-cache \
    bash \
    curl \
    git \
    jq \
    wget \
    ca-certificates \
    tar \
    gzip \
    build-base \
    libffi-dev

# Install just (command runner) using official install script
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin && \
    /usr/local/bin/just --version

# Install osv-scanner
RUN curl -L -f https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64 -o /usr/local/bin/osv-scanner && \
    chmod +x /usr/local/bin/osv-scanner && \
    /usr/local/bin/osv-scanner --version || echo "osv-scanner installed but version check failed"

# Install uv (modern Python package and version manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    export PATH="$HOME/.local/bin:$PATH" && \
    uv --version

# Install Python using uv
RUN export PATH="$HOME/.local/bin:$PATH" && \
    uv python install 3.13 && \
    uv python pin 3.13

# Install semgrep using uv tool install
RUN export PATH="$HOME/.local/bin:$PATH" && \
    uv tool install semgrep && \
    semgrep --version || echo "semgrep version check failed"

# Now use chainguard/python as the final base for better Python support
FROM cgr.dev/chainguard/python:latest

# Switch to root for setup
USER root

# Copy tools from builder stage
COPY --from=tool-builder /usr/local/bin/just /usr/local/bin/just
COPY --from=tool-builder /usr/local/bin/osv-scanner /usr/local/bin/osv-scanner

# Copy system tools needed for development  
COPY --from=tool-builder /usr/bin/wget /usr/local/bin/wget

# Copy uv and uv-managed Python installation
COPY --from=tool-builder /root/.local/bin/uv /usr/local/bin/uv
COPY --from=tool-builder /root/.local/share/uv /root/.local/share/uv
COPY --from=tool-builder /root/.local/bin/semgrep /usr/local/bin/semgrep

# Copy system dependencies needed by Python and tools
COPY --from=tool-builder /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1

# Set up environment for uv and Python
ENV UV_SYSTEM_PYTHON=1
ENV PATH="/usr/local/bin:/root/.local/bin:$PATH"
ENV PYTHONPATH="/workspace/src"

# Create symlink for python3 command to use the existing Python from chainguard
RUN ln -sf /usr/bin/python3 /usr/local/bin/python3

# Create workspace directory and set up node user (for compatibility)
RUN addgroup -g 1000 node && \
    adduser -u 1000 -G node -s /bin/sh -D node && \
    mkdir -p /home/node && \
    chown -R node:node /home/node

# Create workspace directory
RUN mkdir -p /workspace && chown node:node /workspace

# Switch to node user
USER node
WORKDIR /workspace

# Expose common development ports
EXPOSE 3000 5000 8000 8080

# Override the default Python entrypoint to use shell for development
ENTRYPOINT ["/bin/sh"]
CMD ["-l"]
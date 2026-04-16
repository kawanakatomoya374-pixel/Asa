# Dockerfile - Build CppOS in a container
FROM ubuntu:22.04

# Install build tools
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nasm \
    make \
    qemu-system-x86 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /cppos

# Copy source files
COPY . .

# Build command
CMD ["make"]

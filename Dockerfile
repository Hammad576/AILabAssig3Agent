# Use Ubuntu 20.04 as base for compatibility and full environment
FROM ubuntu:20.04

# Set working directory inside the container
WORKDIR /app

# Set non-interactive frontend to avoid prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Python, SWI-Prolog, and pyswip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    swi-prolog \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir pandas numpy pyswip watchdog

# Set environment variables for SWI-Prolog and pyswip
ENV SWI_HOME_DIR=/usr/lib/swi-prolog
ENV LD_LIBRARY_PATH=/usr/lib/swi-prolog/lib:$LD_LIBRARY_PATH
ENV PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH

# Command to run the main Python agent with file watching
CMD ["python3", "runme.py"]
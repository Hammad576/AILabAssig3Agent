# Use Ubuntu 20.04 as base for compatibility and full environment
FROM ubuntu:20.04

# Set working directory inside the container
WORKDIR /app

# Set non-interactive frontend to avoid prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies and add SWI-Prolog PPA
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:swi-prolog/stable \
    && apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    swi-prolog \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    g++ \
    make \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with pinned pyswip version
RUN pip3 install --no-cache-dir pandas numpy pyswip==0.2.10

# Set environment variables for SWI-Prolog and pyswip
ENV SWI_HOME_DIR=/usr/lib/swi-prolog
ENV LD_LIBRARY_PATH=/usr/lib/swi-prolog/lib:$LD_LIBRARY_PATH
ENV PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH

# Start an interactive bash shell
CMD ["bash"]
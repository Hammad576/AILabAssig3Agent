# Use Ubuntu 20.04 as base for compatibility
FROM ubuntu:20.04

# Set working directory
WORKDIR /app

# Set non-interactive frontend for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for SWI-Prolog and Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    g++ \
    make \
    cmake \
    libgmp-dev \
    libssl-dev \
    libpcre3-dev \
    libyaml-dev \
    libncurses5-dev \
    libarchive-dev \
    wget \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install SWI-Prolog 8.4.3 from source, disabling documentation
RUN wget https://www.swi-prolog.org/download/stable/src/swipl-8.4.3.tar.gz \
    && tar -xzf swipl-8.4.3.tar.gz \
    && cd swipl-8.4.3 \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DSWIPL_BUILD_DOCUMENTATION=OFF .. \
    && make -j$(nproc) \
    && make install \
    && cd ../.. \
    && rm -rf swipl-8.4.3 swipl-8.4.3.tar.gz

# Install Python dependencies
RUN pip3 install --no-cache-dir pandas numpy pyswip==0.3.0

# Set environment variables for SWI-Prolog and pyswip
ENV SWI_HOME_DIR=/usr/local/lib/swipl
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH

# Start interactive bash shell
CMD ["bash"]
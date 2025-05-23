# Use Ubuntu 20.04 as base
FROM ubuntu:20.04

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip libjpeg-dev zlib1g-dev gcc g++ make cmake \
    libgmp-dev libssl-dev libpcre3-dev libyaml-dev libncurses5-dev nano wget \
    && rm -rf /var/lib/apt/lists/*

# Install SWI-Prolog 8.4.3
RUN wget https://www.swi-prolog.org/download/stable/src/swipl-8.4.3.tar.gz \
    && tar -xzf swipl-8.4.3.tar.gz \
    && cd swipl-8.4.3 \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=/usr/local .. \
    && make -j$(nproc) \
    && make install \
    && cd ../.. \
    && rm -rf swipl-8.4.3 swipl-8.4.3.tar.gz

# Install Python dependencies
RUN pip3 install --no-cache-dir pandas numpy pyswip==0.3.0

# Set environment variables
ENV SWI_HOME_DIR=/usr/local/lib/swipl
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH

CMD ["bash"]
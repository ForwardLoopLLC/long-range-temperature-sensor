FROM library/gcc
RUN \
        apt-get update && \
        apt-get install -y \
            python-smbus \
            python-dev \
            i2c-tools
RUN \
        echo "i2c-dev" >> /etc/modules
RUN \
        apt-get install -y libi2c-dev

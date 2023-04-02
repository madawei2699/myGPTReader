# Build Python service
FROM python:3.9 AS python-build
WORKDIR /app/gpt-bot
COPY app/gpt-bot/requirements.txt .
COPY app/gpt-bot .

# Build Node.js service
FROM node:14 AS node-build
WORKDIR /app/gpt-reader
COPY app/gpt-reader/package*.json .
RUN npm ci
COPY app/gpt-reader .

# Final image
FROM node:14
WORKDIR /app

# Replace the original sources.list
RUN echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib\n\
	deb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib\n\
	deb http://mirrors.aliyun.com/debian-security buster/updates main\n\
	deb-src http://mirrors.aliyun.com/debian-security buster/updates main\n\
	deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\n\
	deb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\n\
	deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib\n\
	deb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" > /etc/apt/sources.list

# Install Python and other dependencies
RUN apt-get update && \
	apt-get install -y curl gnupg2 software-properties-common && \
	apt-get install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev libffi-dev && \
	curl -O https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz && \
	tar -xf Python-3.9.0.tgz && \
	cd Python-3.9.0 && \
	./configure --enable-optimizations && \
	make -j "$(nproc)" && \
	make altinstall && \
	cd .. && \
	rm -rf Python-3.9.0* && \
	apt-get install -y python3-pip ffmpeg supervisor && \
	curl https://sh.rustup.rs -sSf | sh -s -- -y && \
	echo 'source $HOME/.cargo/env' >> $HOME/.bashrc && \
	/bin/bash -c "source $HOME/.bashrc" && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* && \
	export PATH="$HOME/.cargo/bin:$PATH"

# Set Cargo home directory and add it to the PATH variable
ENV CARGO_HOME="/usr/local/cargo"
ENV PATH="/usr/local/cargo/bin:${PATH}"

# Copy Python service from python-build stage
COPY --from=python-build /app/gpt-bot /app/gpt-bot

# Copy requirements.txt from the python-build stage
COPY --from=python-build /app/gpt-bot/requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy Node.js service from node-build stage
COPY --from=node-build /app/gpt-reader /app/gpt-reader

# Add the python executable path to the PATH variable
ENV PATH="/usr/local/bin:${PATH}"

# Copy supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for both services (change these if your services use different ports)
EXPOSE 50051 5000

# Start supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# Get docker image
FROM node:lts-buster-slim

# Set working dir
WORKDIR /app

# Transfer all our stuff to the builder
COPY . /app/

# Copy start script (Will set the host variable in default.js (overwrite))
COPY start.sh /usr/local/bin/start.sh

# Install cordova
# Also install shelljs because of windows for some reason
RUN npm install --silent -g cordova \
    && npm install --silent -g shelljs \
    && npm install -y --silent

# Run start script (set host and start)
CMD ["/bin/bash", "/usr/local/bin/start.sh"]
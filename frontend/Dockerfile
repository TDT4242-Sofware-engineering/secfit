# Get docker image
FROM node:lts-buster-slim

# Import groupid and host environment variable
ARG GROUPID
ARG DOMAIN
ARG URL_PREFIX
ARG PORT_PREFIX

# Set working dir
WORKDIR /app

# Transfer all our stuff to the builder
COPY . /app/

# Set the host variable in default.js (overwrite)
RUN echo "const HOST = 'https://secfit.vassbo.as';" > ./www/scripts/defaults.js

# Install cordova
# Also install shelljs because of windows for some reason
RUN npm install --silent -g cordova \
    && npm install --silent -g shelljs

# Run cordova app
CMD [ "cordova", "run", "browser", "--release", "--port=3000" ]

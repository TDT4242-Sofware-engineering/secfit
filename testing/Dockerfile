# Get docker image
FROM buildkite/puppeteer:7.1.0

# Set working dir
WORKDIR /app

# Transfer all our stuff to the builder
COPY . /app/

RUN npm install -y --silent 

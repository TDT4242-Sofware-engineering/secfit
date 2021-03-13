#! /bin/bash
# This script makes docker swarm pull new images and restart services using the new images
docker stack deploy --compose-file /home/github/secfit/docker-compose.yml --with-registry-auth stack-secfit
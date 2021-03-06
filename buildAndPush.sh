#! /bin/bash
# This script is for testing build and push.
# It builds all images and push them to docker hub

sudo docker build -f ./frontend/Dockerfile -t jonev/secfit:frontend ./frontend
sudo docker push jonev/secfit:frontend

sudo docker build -f ./backend/secfit/Dockerfile -t jonev/secfit:backend ./backend/secfit
sudo docker push jonev/secfit:backend
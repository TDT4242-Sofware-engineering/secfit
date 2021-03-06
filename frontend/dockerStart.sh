#!/usr/bin/env bash
# dockerStart.sh
# This file runs at container startup
echo "const HOST = '${HOST}';" > ./www/scripts/defaults.js

cordova run browser --release --port=3000
#!/usr/bin/env bash
# start.sh
echo "const HOST = '${HOST}';" > ./www/scripts/defaults.js

cordova run browser --release --port=3000
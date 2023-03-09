#!/bin/bash

set -e

cd /home/deploy
git clone https://github.com/NADEE-MJ/peppermint.git

cd /home/deploy/peppermint

#? poetry and fastapi setup
poetry install

#? sveltekit setup
npm install

echo "Ready!"
tail -f /dev/null

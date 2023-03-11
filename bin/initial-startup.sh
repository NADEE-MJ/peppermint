#!/bin/bash

set -e

cd /home/deploy
if [ ! -d peppermint]; then
    git clone https://github.com/NADEE-MJ/peppermint.git
else
    echo "already cloned peppermint, restarting"
fi

cd /home/deploy/peppermint

#? poetry and fastapi setup
poetry install

#? sveltekit setup
npm install

echo "Ready!"
tail -f /dev/null

#!/bin/bash

set -e

#? poetry and fastapi setup
cd ~/peppermint && poetry install

#? sveltekit setup
cd ~/peppermint && npm install

echo "Ready!"
tail -f /dev/null

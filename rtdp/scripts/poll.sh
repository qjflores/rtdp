#!/usr/bin/env bash

# shell script to run background python process
set -e
export PYTHONPATH='.'
python -u ./rtdp/publisher/poll.py
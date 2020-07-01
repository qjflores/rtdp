#!/usr/bin/env bash
# Exit immediately if a pipeline returns a non-zero status
set -e


pytest --cov=. --cov-report xml --log-cli-level=INFO -s -vv tests/unit

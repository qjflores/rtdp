#!/usr/bin/env bash
# Exit immediately if a pipeline returns a non-zero status
set -e

# Run pylint on all files
IGNORE_PATTERN="" # Leave this blank if you want all files to be linted
(find . -iname "*.py" ! -path "*/\.*" ! -path "$IGNORE_PATTERN") | xargs pylint --rcfile pylintrc -j8

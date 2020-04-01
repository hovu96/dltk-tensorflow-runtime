#!/bin/bash
set -e
set -x

# worker
docker build --rm -f "./worker/thin.Dockerfile" -t hovu96/dltk-tensorflow-runtime:worker-thin .
docker push hovu96/dltk-tensorflow-runtime:worker-thin

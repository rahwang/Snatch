#!/bin/bash
cd ./snatch
poetry run python -m pytest "$@" ../tests/

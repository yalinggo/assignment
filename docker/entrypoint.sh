#!/bin/bash
ENV_FILE=${ENV_FILE:-env/default.env}
export $(grep -v '^#' "$ENV_FILE" | xargs)
python src/main.py
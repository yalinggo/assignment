#!/bin/bash

export $(grep -v '^#' env/default.env | xargs)
python src/main.py
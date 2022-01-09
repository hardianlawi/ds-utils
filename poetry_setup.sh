#!/bin/bash

# Initialize poetry project
poetry init

# General development dependencies
poetry add -D black
poetry add -D flake8
poetry add -D mypy
poetry add -D pre-commit
poetry add -D pytest
poetry add -D "coverage[toml]"
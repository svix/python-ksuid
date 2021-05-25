#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place ksuid --exclude=__init__.py
isort ksuid
black ksuid

#!/usr/bin/env bash

set -ex

mypy .
isort --check-only .
black . --check
flake8 .

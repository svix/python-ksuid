#!/usr/bin/env bash

set -ex

mypy ksuid
isort --check-only ksuid
black ksuid --check
flake8 ksuid

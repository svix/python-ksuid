#!/usr/bin/env bash

set -exu

ty check ksuid
ruff check ksuid
ruff format --check ksuid

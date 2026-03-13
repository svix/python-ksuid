#!/usr/bin/env bash

set -exu

ruff check --fix ksuid
ruff format ksuid

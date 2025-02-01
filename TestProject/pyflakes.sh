#!/bin/bash

echo "============================================================"
echo "== pyflakes =="
pyflakes ../src/awl | grep -v migration

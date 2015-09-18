#!/bin/bash

echo "============================================================"
echo "== pyflakes =="
pyflakes awl | grep -v migration

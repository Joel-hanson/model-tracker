#!/bin/env bash

echo "Running devcontainer post script"

python3 -c "import django; print(django.get_version())"

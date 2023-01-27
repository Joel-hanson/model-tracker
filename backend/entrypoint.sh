#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
make migrate

# Start server
echo "Starting server"
make run

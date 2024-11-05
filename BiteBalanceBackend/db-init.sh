#!/bin/bash
set -e

# Create the testing database
psql -U postgres -c "CREATE DATABASE bitebalance_test;"

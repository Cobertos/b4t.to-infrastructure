#!/bin/bash
# Exit on error
set -e

# Run the backup webservice in the background
python3 /batto-seafile-db-backup-svc.py &

# Run the entrypoint of parent container
exec /usr/local/bin/docker-entrypoint.sh "$@"
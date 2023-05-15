#!/usr/bin/env bash
set -e

if [[ "$ENABLE_MIGRATION" ]]; then
    echo "Applying migrations"
    poetry run alembic upgrade head
    echo "Done"
fi

echo "Starting application"
exec "$@"

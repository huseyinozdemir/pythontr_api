#!/bin/sh
# wait_for_db.sh

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD="$DB_PASS" psql -h "$host" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "Connection the Database - Waiting..."
  sleep 1
done 

>&2 echo "Connect the Database - Working: $cmd"

exec $cmd

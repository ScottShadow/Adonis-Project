#!/bin/bash

# Usage: ./wait-for-it.sh <host>:<port> -- <command>

host="$1"
shift
port="$1"
shift

until nc -z "$host" "$port"; do
  echo "Waiting for MySQL to start..."
  sleep 2
done

echo "MySQL is up - executing command."
exec "$@"

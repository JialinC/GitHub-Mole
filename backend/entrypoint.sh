#!/bin/sh

# Wait for the database to be ready
while ! nc -z $MYSQL_DATABASE_HOST 3306; do
  echo "Waiting for the database..."
  sleep 1
done

# Run migrations
flask db upgrade

# Start the application
exec "$@"
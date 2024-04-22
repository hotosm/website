#!/bin/sh

# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.

# Migrate database
echo "Create database migrations"
python manage.py makemigrations
echo "Apply database migrations"
python manage.py migrate

# Apply localizations
echo "Apply localizations"
python manage.py makemessages -l en
python manage.py makemessages -l fr
python manage.py makemessages -l es
python manage.py compilemessages

# Collect static
echo "Collect static files"
python manage.py collectstatic --noinput --clear

# Create superuser
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    echo "Superuser credentials not provided, skipping superuser creation."
else
    echo "Creating superuser $DJANGO_SUPERUSER_USERNAME"
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
fi

# Start server
echo "Running command: $@"
exec "$@"

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
    echo "Ensuring superuser $DJANGO_SUPERUSER_USERNAME exists"
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "$DJANGO_SUPERUSER_USERNAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created:", username)
else:
    print("Superuser already exists:", username)
EOF
fi

# Start server
echo "Running command: $@"
exec "$@"

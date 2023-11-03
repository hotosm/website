#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser
echo "Creating superuser"
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    echo "Superuser credentials not provided, skipping superuser creation."
else
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
fi

# Start server
echo "Starting server"
gunicorn hot_osm.wsgi:application

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["hotosm-production.fly.dev", "hotosm-staging-new.fly.dev", "*.fly.dev", "127.0.0.1", "localhost", "hotosm.org", "www.hotosm.org", "new-www.hotosm.org"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# AWS S3 Configuration
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-west-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_S3_SIGNATURE_VERSION = 's3v4'  # Use signature version 4 for better compatibility

# S3 File Settings
AWS_DEFAULT_ACL = None  # Bucket owner enforced - ACLs disabled
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = True
AWS_QUERYSTRING_AUTH = False

# Storage backends (Django 4.2+ format)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

try:
    from .local import *
except ImportError:
    pass

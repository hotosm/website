from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

_default_allowed_hosts = [
    "hotosm-production.fly.dev",
    "hotosm-staging-new.fly.dev",
    "hotosm.org",
    "www.hotosm.org",
    "website.hotosm.org",
]
_env_allowed_hosts = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]
ALLOWED_HOSTS = _env_allowed_hosts or _default_allowed_hosts

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Remove XFrameOptionsMiddleware to allow YouTube embeds
MIDDLEWARE = [m for m in MIDDLEWARE if m != 'django.middleware.clickjacking.XFrameOptionsMiddleware']

# Set referrer policy to allow YouTube embeds to work
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Behind the nginx ingress controller (TLS terminated at the LB, plain HTTP
# forwarded to the pod with X-Forwarded-Proto: https).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
# Kubelet liveness/readiness probes hit the pod directly over HTTP with no
# X-Forwarded-Proto header; without this exemption the redirect would fail
# every probe.
SECURE_REDIRECT_EXEMPT = [r"^__lbheartbeat__$"]

# AWS S3 Configuration
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-1")
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

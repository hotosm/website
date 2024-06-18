from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["hotosm-staging-new.fly.dev", "127.0.0.1", "localhost"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + ["django_browser_reload"]  # noqa: F405
MIDDLEWARE = MIDDLEWARE + ["django_browser_reload.middleware.BrowserReloadMiddleware"]  # noqa: F405

try:
    from .local import *
except ImportError:
    pass

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + ["django_browser_reload", "pattern_library",]  # noqa: F405
MIDDLEWARE = MIDDLEWARE + ["django_browser_reload.middleware.BrowserReloadMiddleware"]  # noqa: F405

X_FRAME_OPTIONS = "SAMEORIGIN"

TEMPLATES[0]["OPTIONS"]["builtins"] = ["pattern_library.loader_tags"]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "LOCATION": os.path.join(BASE_DIR, "media"),
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

try:
    from .local import *
except ImportError:
    pass

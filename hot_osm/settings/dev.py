from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + [  # noqa: F405
    "debug_toolbar",
    "django_browser_reload",
    "pattern_library",
]

_locale_middleware_index = MIDDLEWARE.index("django.middleware.locale.LocaleMiddleware")  # noqa: F405
MIDDLEWARE = (
    MIDDLEWARE[: _locale_middleware_index + 1]  # noqa: F405
    + ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    + MIDDLEWARE[_locale_middleware_index + 1 :]  # noqa: F405
    + ["django_browser_reload.middleware.BrowserReloadMiddleware"]
)

INTERNAL_IPS = [
    "127.0.0.1",
]

# Show the toolbar in Docker dev where the client IP is not 127.0.0.1.
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}

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

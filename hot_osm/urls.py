from django.apps import apps
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# from search import views as search_views

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if apps.is_installed("pattern_library"):
        urlpatterns += [
            path("pattern-library/", include("pattern_library.urls")),
        ]

urlpatterns.extend(
    i18n_patterns(
        # For anything not caught by a more specific rule above, hand over to
        # Wagtail's page serving mechanism. This should be the last pattern in
        # the list:
        path("", include(wagtail_urls)),
        # path("search/", search_views.search, name="search"),
        # Alternatively, if you want Wagtail pages to be served from a subpath
        # of your site, rather than the site root:
        #    path("pages/", include(wagtail_urls)),
    )
)

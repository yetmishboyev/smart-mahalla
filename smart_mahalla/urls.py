from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
)

urlpatterns += [
    path("bot/", include("core.urls")),
    path("rosetta/", include("rosetta.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
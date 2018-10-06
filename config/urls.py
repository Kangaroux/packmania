from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import app.views


urlpatterns = [
  path("admin/", admin.site.urls),
  path("api/", include(([
    path("", include("user.urls")),
    path("", include("song.urls")),
  ], "api"))),
  path("", app.views.main)
]

if settings.TESTING:
  urlpatterns.append(path("error_500/", app.views.Dummy500View.as_view(), name="dummy_500"))
  urlpatterns.append(path("error_csrf/", app.views.DummyCSRFView.as_view(), name="dummy_csrf"))
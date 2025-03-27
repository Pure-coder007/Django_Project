

from django.contrib import admin
from django.urls import path, include

url_version = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{url_version}/auth/", include("authentication.urls")),
    path(f"{url_version}/accounts/", include("accounts.urls")),
]

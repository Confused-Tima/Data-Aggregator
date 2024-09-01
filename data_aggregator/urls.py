"""
Main Django URLs
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include(("users.urls", "users"), namespace="users")),
    path(
        "api/",
        include(("data_processor.urls", "data_processor"), namespace="data_processor"),
    ),
]

# insert_csv_data
from django.urls import path

from . import views


urlpatterns = [
    path("file_upload/", views.insert_csv_data, name="file_upload"),
    path(
        "get_products_summary/", views.get_products_summary, name="get_products_summary"
    ),
]

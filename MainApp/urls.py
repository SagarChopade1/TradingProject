from django.urls import path
from MainApp import views

urlpatterns = [
    path("trading/", views.AsyncTradingView.as_view(), name="trading"),
    path(
        "download/<str:file_name>/",
        views.FileDownloadView.as_view(),
        name="download_candle_data",
    ),
]

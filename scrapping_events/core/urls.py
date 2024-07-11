from core import views as core_views
from django.urls import path

urlpatterns = [
    path("search/", core_views.SearchEventAPIView.as_view(), name="search_event"),
]

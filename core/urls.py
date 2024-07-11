from django.urls import path

from core import views as core_views

urlpatterns = [
    path("search/", core_views.SearchEventAPIView.as_view(), name="search_event"),
]

from django.urls import path
from .views import Home,JobSearchView
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('search/',JobSearchView.as_view(),name="search")
]

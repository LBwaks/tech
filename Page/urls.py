from django.urls import path
from .views import Home,JobSearchView,ContactView
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('search/',JobSearchView.as_view(),name="search"),
    path('contact-us/',ContactView.as_view(),name="contact"),
    # path('404',fourView.as_view(),name="404")
]

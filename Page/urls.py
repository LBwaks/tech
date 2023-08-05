from django.urls import path
from .views import Home,JobSearchView,ContactView,FaqListView,About
# app_name = 'Page'
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('search/',JobSearchView.as_view(),name="search"),
    path('contact-us/',ContactView.as_view(),name="contact"),
    path('faq/',FaqListView.as_view(),name="faq"),
    path('about-us/',About.as_view(),name="about"),
    # path("service-detail/<slug>/", ServiceDetailView.as_view(), name="service-detail")
    
]

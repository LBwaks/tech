from django.urls import path
from .views import ApplicationDetailView,ApplicationCreateView
urlpatterns = [
    # path('',JobListView.as_view(),name='jobs'),
    path('applications-details/<slug>',ApplicationDetailView.as_view(),name='applications-details'),
    path('apply-job/<slug>',ApplicationCreateView.as_view(),name='apply-job')
]



from django.urls import path
from .views import JobListView,JobDetailView,JobCreateView
urlpatterns = [
    path('',JobListView.as_view(),name='jobs'),
    path('job-details/<slug>',JobDetailView.as_view(),name='job-details'),
    path('add-jobs/',JobCreateView.as_view(),name='add-jobs')
]



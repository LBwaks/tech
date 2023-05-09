from django.urls import path

from .views import (
    ApplicationCreateView,
    ApplicationDeleteView,
    ApplicationDetailView,
    ApplicationUpdateView,
    MyApplicationsView,
    ApplicationStatusUpdateView,
)
app_name = 'applications'
urlpatterns = [
    # path('',JobListView.as_view(),name='jobs'),
    path(
        "application-details/<uuid:slug>",
        ApplicationDetailView.as_view(),
        name="application-details",
    ),
    path("apply-job/<slug>", ApplicationCreateView.as_view(), name="apply-job"),
    path(
        "update-application/<slug>",
        ApplicationUpdateView.as_view(),
        name="update-application",
    ),
    path('delete-application/<pk>',ApplicationDeleteView.as_view(),name='delete-application'),
    path("my-applications/", MyApplicationsView.as_view(), name="my-applications"),
    path('approve-application/<uuid:pk>',ApplicationStatusUpdateView.as_view(),name='approve-application')
]

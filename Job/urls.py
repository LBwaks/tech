from django.urls import path

from .views import (
    JobCreateView,
    JobDeleteView,
    JobDetailView,
    JobListView,
    JobUpdateView,
    MyJobListView,
    SavedJobListView,
    savedJob,
    JobsByUserView,
    JobsByCategoryView,
    JobsByTagView,
    JobApplicationsListView,
    JobFilterView,
    ApplicationApprovalView,
    ApplicationCancelView,
    MakePaymentView,
   
)

urlpatterns = [
    path("", JobListView.as_view(), name="jobs"),
    path("job-details/<slug>", JobDetailView.as_view(), name="job-details"),
    path("add-jobs/", JobCreateView.as_view(), name="add-jobs"),
    path("update-job/<slug>", JobUpdateView.as_view(), name="update-job"),
    path("delete-job/<slug>", JobDeleteView.as_view(), name="delete-job"),
    path("save-job/<slug>", savedJob, name="save-job"),
    path("saved-jobs/", SavedJobListView.as_view(), name="saved-jobs"),
    path("my-jobs/", MyJobListView.as_view(), name="my-jobs"),
    path("jobs-filter/", JobFilterView.as_view(), name="jobs-filter"),
    path("user-jobs/<username>", JobsByUserView.as_view(), name="user-jobs"),
    path("category-jobs/<slug>", JobsByCategoryView.as_view(), name="category-jobs"),
    path("tag-jobs/<slug>", JobsByTagView.as_view(), name="tag-jobs"),
    path('job/<slug>/applications/', JobApplicationsListView.as_view(), name='job-applications'),
    path('approve-application/<uuid:pk>',ApplicationApprovalView.as_view(),name='approve-application'),     
    path('application/<uuid:pk>/cancel/', ApplicationCancelView.as_view(), name='cancel-application'),
    path('make-payment/', MakePaymentView.as_view(), name='make-payment'),
     
]

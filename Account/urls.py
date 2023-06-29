from django.urls import path
from .views import ProfileUpdateView,UserProfile,deleteEducation,deleteExperience

urlpatterns = [
    path('update-profile/<slug>',ProfileUpdateView.as_view(),name="update-profile"),
    path('user-profile/<slug>',UserProfile.as_view(),name='user-profile'),
    path('remove-education/<slug>',deleteEducation,name="remove-education"),
    path('remove-experience/<slug>',deleteExperience,name="remove-experience")
]
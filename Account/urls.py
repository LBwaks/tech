from django.urls import path
from .views import ProfileUpdateView,UserProfile

urlpatterns = [
    path('update-profile/<slug>',ProfileUpdateView.as_view(),name="update-profile"),
    path('user-profile/<slug>',UserProfile.as_view(),name='user-profile')
]
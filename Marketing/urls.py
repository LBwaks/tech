from django.urls import path
from.views import subscribe,mailchimp_ping_view,unsubscribe

urlpatterns = [
    path('ping/',mailchimp_ping_view),
    path('subscribe',subscribe,name="subscribe"),
    path('unsubscribe',unsubscribe,name="unsubscribe")
]

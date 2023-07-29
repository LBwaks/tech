from django.urls import path
from .views import BlogListView,search,BlogDetailView,CategoryListView
urlpatterns = [
    path("", BlogListView.as_view(), name="blogs"),
    path("search", search, name="blog-search"),
    path("blog-details/<slug>", BlogDetailView.as_view(), name="blog-details"),
    path("category/<slug>", CategoryListView.as_view(), name="category")
]

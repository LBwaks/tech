"""
URL configuration for Technical project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import handler404
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.defaults import page_not_found
from Page.sitemaps import StaticViewSitemap
from Job.sitemaps import JobSitemap
sitemaps={
    "jobs":JobSitemap,
    "static":StaticViewSitemap
}
urlpatterns = [
    path('admin/defender/', include('defender.urls')), # defender admin
    path('admin/', admin.site.urls),
    path("jobs/", include("Job.urls")),
    path("marketing/" , include("Marketing.urls")),
    path("blogs/", include("Blog.urls")),
    path("applications/", include("Application.urls")),
    path("", include("Page.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
#    path('mpesa/', include(mpesa_urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path("profile/", include("Account.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("accounts/", include("allauth.urls")),
    path('hijack/', include('hijack.urls')),
    path('sitemap.xml',sitemap,{"sitemaps":sitemaps},name="django.contrib.sitemaps.views.sitemap"),
    
    # path("hitcount/", include(("hitcount.urls", "hitcount"), namespace="hitcount")),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 ='Page.views.error_404'
# handler500 ='Page.views.error_500'
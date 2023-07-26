from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq ="yearly"
    priority = 0.5
    
    def items(self):
        return ["home","contact"]
    def location(self,item):
        return reverse(item)
    content_type = 'application/xml'
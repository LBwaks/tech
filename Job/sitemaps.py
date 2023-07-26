from django.contrib.sitemaps import  Sitemap
from .models import Job

class JobSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9
    
    def items(self):
        return Job.objects.filter(status="Open")
    
    def lastmod(self,obj):
        return obj.created
    content_type = 'application/xml'
    
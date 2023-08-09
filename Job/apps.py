from django.apps import AppConfig


class JobConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Job"
    
    def ready(self):
        # import Job.signals 
        from . import signals
       

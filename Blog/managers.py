# from .models import Category
from django.db import models
class CategoryManager(models.Manager):
    def get_queryset(self):
        queryset = super(CategoryManager, self).get_queryset().filter(is_published=True)
        queryset = queryset # TODO
        return queryset
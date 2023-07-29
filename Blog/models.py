from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from Blog.managers import CategoryManager
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from .validators import validate_file_size
from django.core.validators import FileExtensionValidator

ext_validator=FileExtensionValidator(['jpg','png','jpeg','gif'])
# Create your models here.
class Category(models.Model):
    """Model definition for Category."""

    # TODO: Define fields here
    user = models.ForeignKey(
        User,
        related_name="category",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from="name")
    description = models.TextField(max_length=250)
    is_published = models.BooleanField(default=True)
    objects = models.Manager()
    publishedCategory =CategoryManager()
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name
    def my_slugify_function(self,content):
        return content.replace("_","-").lower()
    # def save(self).
    #     """Save method for Category."""
    #     pass

    # def get_absolute_url(self):
    #     """Return absolute url for Category."""
    #     return ('')

    # TODO: Define custom methods here
    def similar_objects(self, num_objects=5):
        # Get similar blogs based on the same category
        similar_blogs = Blog.objects.filter(category=self)[:num_objects]
        return similar_blogs

# class TaggedBlog(TaggedItemBase):
#     content_object = models.ForeignKey('Blog', on_delete=models.CASCADE)
class Blog(models.Model):
    """Model definition for Blog."""

    # TODO: Define fields here
    user = models.ForeignKey(
        User, verbose_name=_("blog_author"), on_delete=models.CASCADE
    )
    title = models.CharField(_("Title"), max_length=100)
    slug = AutoSlugField(populate_from='title')
    content = RichTextField(_("Content"))
    category = models.ForeignKey(
        "Category", verbose_name=_("blog_category"), on_delete=models.CASCADE
    )
    # tags = TaggableManager(_("Tags"),through=TaggedBlog)
    photo = models.ImageField(
        _("Photo"),
        upload_to="blogs",
       
        max_length=None,
        validators=[validate_file_size,ext_validator],
        
    )

    # hit_count_generic = GenericRelation(
    #     HitCount,
    #     object_id_field="object_pk",
    #     related_query_name="hit_count_generic_relation",
    # )
    objects = models.Manager()
    # publishedBlogs = BlogManager()
   
    is_published = models.BooleanField(_("Is Published"), default=True)
    is_featured = models.BooleanField(_("Is Featured"), default=False)
    updated = models.DateField(_("Updated"), auto_now=True, auto_now_add=False)
    created = models.DateField(_("Created"), auto_now_add=True)

    class Meta:
        """Meta definition for Blog."""

        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering =("-created",)

    def __str__(self):
        """Unicode representation of Blog."""
        return self.title

    # def save(self):
    #     """Save method for Blog."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Blog."""
        return  reverse('blog-details',kwargs={"slug":self.slug})

    # TODO: Define custom methods here

class Comment(models.Model):
    """Model definition for Comment."""

    # TODO: Define fields here
    blog = models.ForeignKey(
        Blog,
        verbose_name=_("blog_comment"),
        related_name="comments",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User, verbose_name=_("blog_user"), on_delete=models.CASCADE
    )
    comment = models.TextField(_("Comment"))
    created = models.DateField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", related_name="replies", null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        """Meta definition for Comment."""

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """Unicode representation of Comment."""
        return str(self.user) + " says " + str(self.comment)

    # def save(self):
    #     """Save method for Comment."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Comment."""
        return ('')

    # TODO: Define custom methods here
    @property
    def chidren(self):
        return Comment.objects.filter(parent=self).reverse()
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

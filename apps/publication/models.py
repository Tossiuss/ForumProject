from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

# Create your models here.


User = get_user_model()

class SlugFieldMixin:
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Teams(SlugFieldMixin, models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, primary_key=True)


class Tag(SlugFieldMixin, models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True)

class Posts(SlugFieldMixin, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Author')
    title = models.CharField(max_length=25)
    slug = models.SlugField(max_length=30, primary_key=True)
    texts = models.TextField()
    image = models.ImageField(upload_to='posts_img/', blank=True, verbose_name='Pictures')
    category = models.ForeignKey(Teams, on_delete=models.PROTECT, related_name='posts', verbose_name='Category')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

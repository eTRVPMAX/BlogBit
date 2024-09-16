from email.mime import image
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True,blank=True,upload_to='images/')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)
            self.slug = f"{self.slug}-{self.id}"
            super().save(update_fields=['slug'])
        else:
            super().save(*args, **kwargs)
            
    def __str__(self):
        return self.title
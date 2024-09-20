from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to='images/')
    tags = models.ManyToManyField('Tag', blank=True, related_name='post')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)
            self.slug = f"{self.slug}-{self.id}"
            super().save(update_fields=['slug'])
        else:
            super().save(*args, **kwargs)
            
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)
            
    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')


    def __str__(self):
        return f"{self.author.username} on '{self.post.title}': {self.content[:20]}"
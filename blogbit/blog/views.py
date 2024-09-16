from multiprocessing import context
from django.shortcuts import render
from .models import BlogPost

# Create your views here.

def post_page(request, slug):
    post =BlogPost.objects.get(slug=slug)
    context = {
        'post': post
    }
    return render(request, 'blog/post.html', context)

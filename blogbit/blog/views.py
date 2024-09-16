from multiprocessing import context
from django.shortcuts import render
from .models import BlogPost

# Create your views here.
def index(request):
    posts = BlogPost.objects.all()
    context = {
        'posts':posts
    }
    return render(request, 'blog/index.html', context)

def post_page(request, slug):
    post =BlogPost.objects.get(slug=slug)
    context = {
        'post': post
    }
    return render(request, 'blog/post.html', context)

from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Tag

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

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag)
    return render(request, 'blog/tagged.html', {'tag': tag, 'posts': posts})
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentForm
from .models import BlogPost, Tag


# Create your views here.
def index(request):
    posts = BlogPost.objects.all()
    context = {
        'posts':posts
    }
    return render(request, 'blog/index.html', context)

def post_page(request, slug):
    post = BlogPost.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_page', slug=post.slug)
    else:
        form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': post.comments.all()
    }
    return render(request, 'blog/post.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag)
    context = {'tag': tag, 'posts': posts}
    return render(request, 'blog/tagged.html', context)

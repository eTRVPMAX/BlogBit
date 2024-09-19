from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentForm, Signupform
from .models import BlogPost, Tag
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)

def post_page(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
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
        
    comments = post.comments.all()
    paginator= Paginator(comments, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'post': post,
        'form': form,
        'page_obj': page_obj
    }
    return render(request, 'blog/post.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag)
    context = {'tag': tag, 'posts': posts}
    return render(request, 'blog/tagged.html', context)


def signup(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = Signupform()
        
    context = {'form': form}
    return render(request, 'registration/signup.html', context)
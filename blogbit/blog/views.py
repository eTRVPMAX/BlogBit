from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentForm, SignupForm, CreatePostForm
from .models import BlogPost, Tag
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
def index(request):
    posts = BlogPost.objects.all().order_by('-created_at')
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
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('post_page', slug=post.slug)
    else:
        form = CommentForm()
        
    comments = post.comments.all().order_by('-date')
    paginator = Paginator(comments, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'post': post,
        'form': form,
        'page_obj': page_obj
    }
    return render(request, 'blog/post.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('/')
    else:
        form = CreatePostForm()
    
    context = {'form': form}
    return render(request, 'blog/create_post.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag).order_by('-created_at')
    context = {'tag': tag, 'posts': posts}
    return render(request, 'blog/tagged.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {form.cleaned_data.get("username")}!')
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
        
    context = {'form': form}
    return render(request, 'registration/signup.html', context)
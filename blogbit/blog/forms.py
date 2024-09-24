from django import forms
from .models import Comment, BlogPost, Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    """
    Form for adding comments to a blog post.
    """
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom widget attributes.
        """
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Comment here...'
        })

class SignupForm(UserCreationForm):
    """
    Form for user registration.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom widget attributes.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Password confirmation'
        })

    def clean_username(self):
        """
        Validate that the username is unique.
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        """
        Validate that the email is unique.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_password2(self):
        """
        Validate that the two password entries match.
        """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

class CreatePostForm(forms.ModelForm):
    """
    Form for creating a new blog post.
    """
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom widget attributes.
        """
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Title'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Content'
        })
        self.fields['tags'].queryset = Tag.objects.all()
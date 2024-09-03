from django.shortcuts import render, redirect
from .models import Blog
from django.shortcuts import get_object_or_404
from .forms import BlogForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def blogs(request):
    message = ''
    if not Blog.objects.exists():
        message = 'No blogs created yet.'
        return render(request, 'blogs.html', {
            'title': 'Blogs',
            'message': message,
        })
    else:
        blogs = Blog.objects.all()
    return render(request, 'blogs.html', {
        'title': 'Blogs',
        'message': message,
        'blogs': blogs,
    })

@login_required
def create_blog(request):
    if request.method == 'POST':
        blog = Blog(title=request.POST['title'],
                    description=request.POST['description'])
        blog.save()
        return redirect('blogs')
    return render(request, 'create_blog.html', {
        'title': 'Create Blog',
    })

@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'delete':
            blog.delete()
        elif action == 'update':
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                form.save()
        return redirect('blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog_detail.html', {
        'title': blog.title,
        'blog': blog,
        'form': form,
    })


def signup(request):
    message = ''
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('create_blog')
            except:
                return render(request, 'signup.html', {
                    'title': 'Signup',
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'title': 'Signup',
                'form': UserCreationForm,
                'error': 'Passwords do not match'
            })
    return render(request, 'signup.html', {
        'form': UserCreationForm,
        'title': 'Signup',
    })

@login_required
def signout(request):
    logout(request)
    return redirect('blogs')

def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'title': 'Log in',
            'form' : AuthenticationForm,
            'error': 'Username or password is incorrect'
        })
        else:
            login(request, user)
            return redirect('blogs')
    return render(request, 'signin.html', {
        'title': 'Log in',
        'form' : AuthenticationForm
    })
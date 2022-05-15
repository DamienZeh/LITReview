from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import BlogForm, PhotoForm
from .models import Blog
from django.shortcuts import get_object_or_404, render, redirect


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'ticket_and_review/view_blog.html', {'blog': blog})

@login_required #permet d'interdire l'accès, si on est pas connecté
def flux_page(request):
    blogs = Blog.objects.all()
    return render(request, 'ticket_and_review/flux.html', context={'blogs': blogs})

@login_required
def photo_upload(request):
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('flux')
    return render(request, 'ticket_and_review/photo_upload.html', context={'form': form})

@login_required
def blog_and_photo_upload(request):
    blog_form = BlogForm()
    photo_form = PhotoForm()
    if request.method == 'POST':
        blog_form = BlogForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            return redirect('flux')
    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
        }
    return render(request, 'ticket_and_review/create_blog_post.html', context=context)

@login_required #permet d'interdire l'accès, si on est pas connecté
def posts_page(request):
    form = None
    return render(request, 'ticket_and_review/posts.html', context={'form': form})

@login_required #permet d'interdire l'accès, si on est pas connecté
def subscription_page(request):
    form = None
    return render(request, 'ticket_and_review/abonnements.html', context={'form': form})


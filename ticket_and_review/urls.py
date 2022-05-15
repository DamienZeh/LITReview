from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import flux_page as flux, posts_page as posts,\
    subscription_page as subscription, blog_and_photo_upload, photo_upload, view_blog

urlpatterns = [
    path('flux/', flux, name="flux"),
    path('posts/', posts, name="posts"),
    path('abonnements/', subscription, name="abonnements"),
    path('photo/upload/', photo_upload, name='photo_upload'),
    path('blog/create', blog_and_photo_upload, name='blog_create'),
    path('blog/<int:blog_id>', view_blog, name='view_blog'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import flux_page as flux, posts_page as posts,\
    subscription_page as subscription, ticket_and_image_upload, image_upload, view_ticket

urlpatterns = [
    path('flux/', flux, name="flux"),
    path('posts/', posts, name="posts"),
    path('abonnements/', subscription, name="abonnements"),
    path('image/upload/', image_upload, name='image_upload'),
    path('ticket/create', ticket_and_image_upload, name='ticket_create'),
    path('ticket/<int:ticket_id>', view_ticket, name='view_ticket'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
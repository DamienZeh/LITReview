from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import flux_page as flux, posts_page as posts,\
    subscription_page as subscription, ticket_and_image_upload, image_upload,\
    view_ticket, edit_ticket, delete_ticket

urlpatterns = [
    path('flux/', flux, name="flux"),
    path('posts/', posts, name="posts"),
    path('subscription/', subscription, name="subscription"),
    path('image/upload/', image_upload, name='image_upload'),
    path('ticket/create', ticket_and_image_upload, name='ticket_create'),
    path('ticket/<int:ticket_id>', view_ticket, name='view_ticket'),
    path('ticket/<int:ticket_id>/edit', edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete', delete_ticket, name='delete_ticket'),
    path('follow-users/', subscription, name='follow_users')
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
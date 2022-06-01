from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import flux_page as flux, posts_page as posts,\
    subscription_page as subscription, ticket_creation, image_upload,\
    view_ticket, edit_post, delete_post, unfollow,\
    review_creation

urlpatterns = [
    path('flux/', flux, name="flux"),
    path('posts/', posts, name="posts"),
    path('subscription/', subscription, name="subscription"),
    path('image/upload/', image_upload, name='image_upload'),
    path('ticket/create', ticket_creation, name='ticket_create'),
    path('review/create/', review_creation, name='review_create'),
    path('ticket/<int:ticket_id>', view_ticket, name='view_ticket'),
    path('ticket/<int:post_id>/edit', edit_post, name='edit_post'),
    path('ticket/<int:post_id>/delete', delete_post, name='delete_post'),
    path('follow-users/', subscription, name='follow_users'),
    path('unfollow/<user_follows_id>', unfollow, name='unfollow'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
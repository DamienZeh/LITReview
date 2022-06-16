from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    flux_page as flux,
    posts_page as posts,
    subscription_page as subscription,
    ticket_creation,
    edit_post,
    delete_post,
    unfollow,
    review_creation,
    auto_review_creation,
)

urlpatterns = [
    path("flux/", flux, name="flux"),
    path("posts/", posts, name="posts"),
    path("subscription/", subscription, name="subscription"),
    path("ticket/create", ticket_creation, name="ticket_create"),
    path("review/create/<int:ticket_id>/", review_creation, name="review_create"),
    path("review/auto_create/", auto_review_creation, name="auto_review_create"),
    path("ticket/<int:obj_id>/edit", edit_post, name="edit_post"),
    path("ticket/<int:obj_id>/delete", delete_post, name="delete_post"),
    path("follow-users/", subscription, name="follow_users"),
    path("unfollow/<user_follows_id>", unfollow, name="unfollow"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

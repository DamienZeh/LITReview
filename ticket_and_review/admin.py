from django.contrib import admin
from .models import Ticket, Review, UserFollows



class TicketAdmin(admin.ModelAdmin):
    """Show ticket's info in admin"""
    list_display = ('title', 'description', 'user', 'image', 'time_created')

class ReviewAdmin(admin.ModelAdmin):
    """Show ticket's info in admin"""
    list_display = ('ticket','headline', 'body', 'user', 'rating', 'time_created')

class UserFollowsAdmin(admin.ModelAdmin):
    """Show userfollows's info in admin"""
    list_display = ('user', 'followed_user')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
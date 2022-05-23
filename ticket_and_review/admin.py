from django.contrib import admin
from .models import Ticket, UserFollows



class TicketAdmin(admin.ModelAdmin):
    """Show ticket's info in admin"""
    list_display = ('title', 'description', 'user', 'time_created')

class UserFollowsAdmin(admin.ModelAdmin):
    """Show userfollows's info in admin"""
    list_display = ('user', 'followed_user')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
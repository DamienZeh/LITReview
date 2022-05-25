from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from .forms import TicketForm, DeleteTicketForm
from .models import Ticket, UserFollows
from itertools import chain

@login_required
def flux_page(request):
    users_followed = []
    for user in UserFollows.objects.filter(user=request.user):
        users_followed.append(user.followed_user)

    tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=users_followed))
    posts = sorted(chain(tickets),
                   key= lambda post: post.time_created, reverse=True)
    return render(request, 'ticket_and_review/flux.html', context={'posts': posts})


@login_required
def posts_page(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket_and_review/posts.html', context={'tickets': tickets})


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_and_review/view_ticket.html', {'ticket': ticket})


@login_required
def image_upload(request):
    form = TicketForm().image
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            # set the uploader to the user before saving the model
            image.uploader = request.user
            # now we can save
            image.save()
            return redirect('flux')
    return render(request, 'ticket_and_review/image_upload.html', context={'form': form})


@login_required
def ticket_and_image_upload(request):
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    context = {
        'ticket_form': ticket_form
        }
    return render(request, 'ticket_and_review/create_ticket_post.html', context=context)


@login_required
def subscription_page(request):
    users_followed = UserFollows.objects.filter(user=request.user)
    users_followers = UserFollows.objects.filter(followed_user=request.user)
    if request.method == 'POST':
        follow = request.POST['name']#get input name's user from html
        username = request.user
        if follow != "":
            to_follow = User.objects.get(username=follow)# User instance
            if to_follow != username : # can't follow yourself
                UserFollows.objects.create(user=request.user, followed_user=to_follow)



    return render(request, 'ticket_and_review/subscription.html',
                  context={'users_followed': users_followed, 'users_followers': users_followers})


@login_required
def unfollow(request, user_follows_id):
    subscription = UserFollows.objects.filter(pk=user_follows_id)
    subscription.delete()
    return redirect('subscription')


@login_required
def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST or None, request.FILES or None, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')

    context = {
        'edit_form': edit_form,
        }
    return render(request, 'ticket_and_review/edit_ticket.html', context=context)
"""
@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = TicketForm(request.POST or None, request.FILES or None, instance=ticket)

            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
    context = {
        'edit_form': edit_form,
        }
    return render(request, 'ticket_and_review/edit_ticket.html', context=context)
"""

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    delete_form = DeleteTicketForm()
    if request.method == 'POST':
        if 'delete_ticket' in request.POST:
            delete_form = DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('posts')
    context = {
        'delete_form': delete_form,
        }
    return render(request, 'ticket_and_review/delete_ticket.html', context=context)


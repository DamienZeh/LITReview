from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from .forms import TicketForm, DeletePostForm, ReviewForm
from .models import Ticket, UserFollows, Review
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import CharField, Value


@login_required
def get_posts(request):
    """
    Get all tickets user and users followed
    """
    users_followed = []
    for user in UserFollows.objects.filter(user=request.user):
        users_followed.append(user.followed_user)

    tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=users_followed))
    reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=users_followed))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    all_posts = sorted(chain(reviews, tickets),
                   key= lambda post: post.time_created, reverse=True)
    return all_posts


@login_required
def flux_page(request):
    posts = get_posts(request)
    return render(request, 'ticket_and_review/flux.html', context={'posts': posts})


@login_required
def posts_page(request):
    posts = get_posts(request)
    return render(request, 'ticket_and_review/posts.html',
                  context={'posts': posts})


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
def ticket_creation(request):
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
def review_creation(request):
    review_form = ReviewForm()
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = ReviewForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            review = review_form.save(commit=False)
            ticket.user = request.user
            review.user = request.user
            ticket.save()
            review.save()

            return redirect('flux')
    context = {
         'review_form': review_form,
        'ticket_form': ticket_form,
        }

    return render(request, 'ticket_and_review/create_review_post.html', context=context)


@login_required
def review_creation_response(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()
    ticket_form = TicketForm()
    if request.method == 'GET':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            ticket_form.instance.user = request.user
            ticket = ticket_form.save()
            review_form.instance.ticket = ticket.pk
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('flux')
    context = {
         'review_form': review_form,
         'ticket': ticket
        }
    return render(request, 'ticket_and_review/create_review_post.html', context=context)


@login_required
def subscription_page(request):
    users_followed = UserFollows.objects.filter(user=request.user)
    users_followers = UserFollows.objects.filter(followed_user=request.user)
    if request.method == 'POST':
        follow = request.POST['name']#get input name's user from html
        username = request.user
        try:
            to_follow = User.objects.get(username=follow)# User instance
            if to_follow != username :
                if UserFollows.objects.get_or_create\
                            (user=request.user, followed_user=to_follow) is False:
                    UserFollows.objects.create(user=request.user, followed_user=to_follow)
                else:
                    messages.add_message(request, messages.INFO, f"Vous êtes abonné à {to_follow}.")
            else:
                messages.add_message(request, messages.INFO, f"Vous êtes {request.user} !")
        except ObjectDoesNotExist:
            messages.add_message(request, messages.INFO, "Cet utilisateur n'existe pas.")

    return render(request, 'ticket_and_review/subscription.html',
                  context={'users_followed': users_followed, 'users_followers': users_followers})


@login_required
def unfollow(request, user_follows_id):
    subscription = UserFollows.objects.filter(pk=user_follows_id)
    subscription.delete()
    return redirect('subscription')


@login_required
def edit_post(request, post_id):
    try:
        post = Ticket.objects.get(id=post_id)
        form = TicketForm
        html =  'ticket_and_review/edit_post.html'
    except ObjectDoesNotExist:
        post = Review.objects.get(id=post_id)
        form = ReviewForm
        html =  'ticket_and_review/edit_review.html'
    edit_form = form(instance=post)
    if request.method == 'POST':
        edit_form = form(request.POST or None, request.FILES or None, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('posts')
    context = {
        'edit_form': edit_form,
        }
    return render(request, html, context=context)


@login_required
def delete_post(request, post_id):
    try:
        post = Ticket.objects.get(id=post_id)
    except ObjectDoesNotExist:
        post = Review.objects.get(id=post_id)
    delete_form = DeletePostForm()
    if request.method == 'POST':
        delete_form = DeletePostForm(request.POST)
        if delete_form.is_valid():
            post.delete()
            return redirect('posts')
    context = {
        'delete_form': delete_form,
        }
    return render(request, 'ticket_and_review/delete_post.html', context=context)




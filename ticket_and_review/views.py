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
def posts(request):
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
    get_posts = posts(request)
    return render(request, 'ticket_and_review/flux.html', context={'posts': get_posts})


@login_required
def posts_page(request):
    get_posts = posts(request)
    return render(request, 'ticket_and_review/posts.html',
                  context={'posts': get_posts})


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
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket_form.instance.user = request.user
            review_form.instance.user = request.user
            ticket = ticket_form.save()
            review_form.instance.ticket = ticket
            review_form.save()

            return redirect('flux')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
        }
    return render(request, 'ticket_and_review/create_ticket_post.html', context=context)



@login_required
def review_upload(request):
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
def review_upload_response(request, ticket_id):
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
def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = TicketForm(request.POST or None, request.FILES or None, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('posts')

    context = {
        'edit_form': edit_form,
        }
    return render(request, 'ticket_and_review/edit_ticket.html', context=context)


@login_required
def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)
    edit_form = ReviewForm(instance=review)
    if request.method == 'POST':
        edit_form = ReviewForm(request.POST or None, request.FILES or None, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('posts')

    context = {
        'edit_form': edit_form,
        }
    return render(request, 'ticket_and_review/edit_review.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    delete_form = DeletePostForm()
    if request.method == 'POST':
        delete_form = DeletePostForm(request.POST)
        if delete_form.is_valid():
            ticket.delete()
            return redirect('posts')
    context = {
        'delete_form': delete_form,
        }
    return render(request, 'ticket_and_review/delete_post.html', context=context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    delete_form = DeletePostForm()
    if request.method == 'POST':
        delete_form = DeletePostForm(request.POST)
        if delete_form.is_valid():
            review.delete()
            return redirect('posts')
    context = {
        'delete_form': delete_form,
        }
    return render(request, 'ticket_and_review/delete_post.html', context=context)


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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
    Get all posts user and users followed
    """
    users_followed = []
    for user in UserFollows.objects.filter(user=request.user):
        users_followed.append(user.followed_user)
    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=users_followed)
    )
    reviews = Review.objects.filter(
        Q(user=request.user)
        | Q(ticket__user=request.user)
        | Q(user__in=users_followed)
    )
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    all_posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )
    return all_posts


@login_required
def flux_page(request):
    """
    get all posts from get_posts() and goes in flux page.
    """
    posts = get_posts(request)
    return render(
        request, "ticket_and_review/flux.html", context={"posts": posts}
    )


@login_required
def posts_page(request):
    """
    get all posts from get_posts() and goes in posts page.
    """
    posts = get_posts(request)
    return render(
        request, "ticket_and_review/posts.html", context={"posts": posts}
    )


@login_required
def ticket_creation(request):
    """
    Create ticket and goes in flux page if ok.
    """
    ticket_form = TicketForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux")
    context = {"ticket_form": ticket_form}
    return render(
        request, "ticket_and_review/create_ticket_post.html", context=context
    )


@login_required
def review_creation(request, ticket_id):
    """
    get ticket id and create review for this ticket.
    """
    review_form = ReviewForm()
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            ticket.review_existing = True
            ticket.save()
            review.user = request.user
            review.save()

            return redirect("flux")
    context = {
        "review_form": review_form,
        "ticket": ticket,
    }
    return render(
        request, "ticket_and_review/create_review_post.html", context=context
    )


@login_required
def auto_review_creation(request):
    """
    Create autoreview (ticket + review).
    """
    form_ticket = TicketForm()
    form_review = ReviewForm()
    if request.method == "POST":
        form_ticket_post = TicketForm(request.POST, request.FILES)
        form_review_post = ReviewForm(request.POST)
        if form_ticket_post.is_valid() and form_review_post.is_valid():
            review_form = form_review_post.save(commit=False)
            ticket_form = form_ticket_post.save(commit=False)
            ticket = Ticket.objects.create(
                title=ticket_form.title,
                description=ticket_form.description,
                user=request.user,
                image=ticket_form.image,
                time_created=ticket_form.time_created,
                review_existing=True,
            )
            review_form.ticket = ticket
            review_form.user = request.user

            ticket.save()
            review_form.save()
            return redirect("flux")
    context = {
        "form_ticket": form_ticket,
        "form_review": form_review,
    }
    return render(
        request,
        "ticket_and_review/create_auto_review_post.html",
        context=context,
    )


@login_required
def subscription_page(request):
    """
    get users_followed and users_followers, and checks if input = user existing
    """
    users_followed = UserFollows.objects.filter(user=request.user)
    users_followers = UserFollows.objects.filter(followed_user=request.user)
    if request.method == "POST":
        follow = request.POST["name"]  # get input name's user from html page.
        username = request.user
        try:
            to_follow = User.objects.get(username=follow)
            if to_follow != username:
                if (
                    UserFollows.objects.get_or_create(
                        user=request.user, followed_user=to_follow
                    )
                    is False
                ):
                    UserFollows.objects.create(
                        user=request.user, followed_user=to_follow
                    )
                else:
                    messages.add_message(
                        request,
                        messages.INFO,
                        f"Vous êtes abonné à {to_follow}.",
                    )
            else:
                messages.add_message(
                    request, messages.INFO, f"Vous êtes {request.user} !"
                )
        except ObjectDoesNotExist:
            messages.add_message(
                request, messages.INFO, "Cet utilisateur n'existe pas."
            )

    return render(
        request,
        "ticket_and_review/subscription.html",
        context={
            "users_followed": users_followed,
            "users_followers": users_followers,
        },
    )


@login_required
def unfollow(request, user_follows_id):
    """
    get user followed id
    delete subscription and redirect to 'subscription'
    """
    if request.method == "GET":
        subscription = UserFollows.objects.filter(pk=user_follows_id)
        subscription.delete()
    return redirect("subscription")


@login_required
def edit_post(request, obj_id):
    """
    get post's id
    edit post if is a ticket, review or autoreview
    """
    try:
        obj = Ticket.objects.get(id=obj_id)
        form = TicketForm
        html = "ticket_and_review/edit_ticket.html"
    except Ticket.DoesNotExist:
        obj = Review.objects.get(id=obj_id)
        form = ReviewForm
        html = "ticket_and_review/edit_review.html"
    edit_form = form(instance=obj)
    if request.method == "POST":
        edit_form = form(
            request.POST or None, request.FILES or None, instance=obj
        )
        if edit_form.is_valid():
            edit_form.save()
            return redirect("posts")
    context = {"edit_form": edit_form, "post": obj}
    return render(request, html, context=context)


@login_required
def delete_post(request, obj_id):
    """
    get post's id
    delete post if is a ticket, review or autoreview
    """
    try:
        obj = Ticket.objects.get(id=obj_id)
    except Ticket.DoesNotExist:
        obj = Review.objects.get(id=obj_id)
    delete_form = DeletePostForm()
    if request.method == "POST":
        delete_form = DeletePostForm(request.POST)
        if delete_form.is_valid():
            if isinstance(obj, Review):
                obj.ticket.review_existing = False
                obj.ticket.save()
            obj.delete()

            return redirect("posts")
    context = {
        "delete_form": delete_form,
    }
    return render(
        request, "ticket_and_review/delete_post.html", context=context
    )

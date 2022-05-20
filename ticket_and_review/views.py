from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import TicketForm, DeleteTicketForm
from .models import Ticket, UserFollows
from django.shortcuts import get_object_or_404, render, redirect


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_and_review/view_ticket.html', {'ticket': ticket})


@login_required
def flux_page(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket_and_review/flux.html', context={'tickets': tickets})


@login_required
def posts_page(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket_and_review/posts.html', context={'tickets': tickets})


@login_required
def image_upload(request):
    form = TicketForm().image
    if request.method == 'POST':
        form =TicketForm(request.POST, request.FILES)
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
    subscription = UserFollows.objects.all()
    return render(request, 'ticket_and_review/subscription.html', context={'subscription': subscription})


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


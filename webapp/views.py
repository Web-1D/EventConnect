from django.shortcuts import render, redirect
from django.http import HttpResponse
from webapp.models import User, Category, Event, Comment, QAForum
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from webapp.forms import CategoryForm, EventForm, UserForm


def home(request):

    category_list = Category.objects.all()
    events = Event.objects.all()
    context_dict = {'categories' : category_list, 'events': events}

    response = render(request, 'webapp/home.html', context=context_dict)
    return response

def contact(request):
    return render(request, 'webapp/contact.html')

def qa(request):
    return render(request, 'webapp/qa.html')

def categories(request, category_name):

    context_dict = {}

    try:
        category = Category.objects.get(name=category_name)
        events = Event.objects.filter(category=category)
        context_dict['events'] = events
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['events'] = None
    
    return render(request, 'webapp/category_detail.html', context_dict)

def event_detail(request, event_id):

    context_dict = {}

    try:
        event = Event.objects.get(id=event_id)
        context_dict['event'] = event
    except Event.DoesNotExist:
        context_dict['event'] = None
    
    return render(request, 'webapp/event_detail.html', context_dict)

def event_comments(request, event_id):

    context_dict = {}

    try:
        event = Event.objects.get(id=event_id)
        context_dict['event'] = event
        context_dict['comments'] = Comment.objects.filter(event=event)
    except Event.DoesNotExist:
        context_dict['event'] = None
        context_dict['comments'] = None
        return HttpResponse("Event not found or permission not granted.")
    
    return render(request, 'webapp/event_comments.html', context_dict)

def signup(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    
    return render(request, 'webapp/signup.html',
                  context = {'user_form': user_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting login for: {username}")

        user = authenticate(username=username, password=password)
        

        if user:
            print(f"Authenticated User: {user}")
            if user.is_active:
                login(request, user)
                return redirect(reverse('webapp:home'))
            else:
                return HttpResponse("Your EventConnect account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    return render(request, 'webapp/user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('webapp:home'))

@login_required
def event_signup(request, event_id):

    context_dict = {}

    try:
        event = Event.objects.get(id=event_id)
        context_dict['event'] = event
    except Event.DoesNotExist:
        context_dict['event'] = None
        return HttpResponse("Event not found.")

    if request.method == 'POST':
        event.attendees.add(request.user)
        
        return redirect(reverse('webapp:event_detail', args=[event_id]))

    return render(request, 'webapp/event_signup.html', context_dict)

@login_required
def add_comment(request, event_id):

    context_dict = {}

    try:
        event = Event.objects.get(id=event_id)
        context_dict['event'] = event
    except Event.DoesNotExist:
        context_dict['event'] = None
        return HttpResponse("Event not found.")

    if request.method == 'POST':
        message = request.POST.get('comment')
        if message:
            Comment.objects.create(user=request.user, event=event, comment=message)
            
            return redirect(reverse('webapp:event_comments', args=[event_id]))
        else:
            return HttpResponse("Comment may not be blank.")
    
    return render(request, 'webapp.add_comment.html', context_dict)

@login_required
def enable_notifications(request, event_id):

    context_dict = {}

    try:
        event = Event.objects.get(id=event_id)
        context_dict['event'] = event
    except Event.DoesNotExist:
        context_dict['event'] = None
        return HttpResponse("Event not found.")

    ## adding to a list of users who want notifications?
    
    return render(request, 'webapp/enable_notifications.html', context_dict)

def organiser_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                if user.role == 'organiser':
                    login(request, user)
                    return redirect(reverse('webapp:organiser_account'))
                else:
                    return HttpResponse("You do not have access to the organiser portal.")
            else:
                return HttpResponse("Your EventConnect account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    return render(request, 'webapp/organiser_login.html')

@login_required
def organiser_account(request):
    events = Event.objects.filter(organiser=request.user)
    return render(request, 'webapp/organiser_account.html', {'events' : events})

@login_required
def add_event(request, category_name):
    
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        return HttpResponse("Category does not exist.")

    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.category = category
            event.organiser = request.user
            event.save()

            return redirect(reverse('webapp:categories',
                                        args=[category.name]))

        else:
            print(form.errors)

            
    context_dict = {'form': form, 'category': category}
    return render(request, 'webapp/add_event.html', context_dict)

@login_required
def edit_event(request, event_id):
    context_dict = {}
    
    try:
        event = Event.objects.get(id=event_id, organiser=request.user)
        context_dict['event'] = event 
    except:
        return HttpResponse("Event not found or permission not granted.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse('webapp:event_detail', args=[event_id]))
        else:
            form = EventForm(instance=event)

    context_dict['form'] = form

    return render(request, 'webapp/edit_event.html', context_dict)

@login_required
def delete_event(request, event_id):

    try:
        event = Event.objects.get(id=event_id, organiser=request.user)
        event.delete()
        return redirect(reverse('webapp:organiser_account'))
    except Event.DoesNotExist:
        return HttpResponse("Event not found or permission not granted.")























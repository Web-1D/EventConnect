from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from webapp.models import User, Category, Event, Comment, QAForum
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from webapp.forms import CategoryForm, EventForm, UserForm
from django.contrib.auth.forms import AuthenticationForm



def home(request):

    all_categories = Category.objects.all()
    predefined = ['Sports', 'Music', 'Academic', 'Cultural']

    main_categories = all_categories.filter(name__in=predefined)
    other_categories = all_categories.exclude(name__in=predefined)

    events = Event.objects.all()

    context_dict = {
        'categories': all_categories,
        'all_categories': all_categories,
        'main_categories': main_categories,
        'other_categories': other_categories,
        'events': events
    }

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

@login_required
def add_category(request):
    if request.user.role != 'organiser':
        return HttpResponse("You are not authorized to add categories")

    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webapp:organiser_account')

    return render(request, 'webapp/add_category.html', {'form': form})


def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return redirect('webapp:home')

    context_dict = {'event': event}
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
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)

            if user.role == 'organiser':
                return redirect('webapp:organiser_account')
            else:
                return redirect('webapp:home')

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'webapp/signup.html',
                  context={'user_form': user_form, 'registered': registered})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(username=username, password=password)

        if user is not None and user.role == role:
            login(request, user)
            if role == 'organiser':
                return redirect('webapp:organiser_account')
            else:
                return redirect('webapp:home')
        else:
            return HttpResponse("Invalid credentials")

    return render(request, 'webapp/login.html')


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


@login_required
def organiser_account(request):
    if request.user.role != 'organiser':
        return redirect('webapp:home')
    events = Event.objects.filter(organiser=request.user)
    categories = Category.objects.all()
    return render(request, 'webapp/organiser_account.html', {
        'events': events,
        'categories': categories,
        'user' : request.user,
    })


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

            
    context_dict = {'form': form, 'category_name': category_name}
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




def ajax_search_events(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        events = Event.objects.filter(title__icontains=query)
        results = [event.title for event in events]
        return JsonResponse(results, safe=False)


def autocomplete_events(request):
    if request.is_ajax():
        term = request.GET.get('term', '')
        events = Event.objects.filter(title__icontains=term)[:10]
        results = [{'title': event.title} for event in events]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


def search_events(request):
    query = request.GET.get('q', '')
    category_name = request.GET.get('category', '')

    events = Event.objects.all()
    if query:
        events = events.filter(title__icontains=query)

    if category_name:
        events = events.filter(category__name__iexact=category_name)

    data = [{
        'id': event.id,
        'title': event.title,
        'date': event.date.strftime('%Y-%m-%d'),
        'location': event.location,
    } for event in events]

    return JsonResponse(data, safe=False)


def search_event_redirect(request):
    if request.method == 'GET':
        title = request.GET.get('search_term', '').strip()
        try:
            event = Event.objects.get(title__iexact=title)
            return redirect('webapp:event_detail', event_id=event.id)
        except Event.DoesNotExist:
            return render(request, 'webapp/search_no_result.html', {'title': title})
















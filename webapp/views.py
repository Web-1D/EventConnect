from django.shortcuts import render
from django.http import HttpResponse

def home(request):

    context_dict = {}
    #context_dict['categories'] = 

    response = render(request, 'webapp/home.html', context=context_dict)
    return response

def contact(request):
    return

def qa(request):
    return render(request, 'webapp/qa.html', context=context_dict)

def category(request, category_name):
    return

def event_detail(request, event_id):
    return

def event_comments(request, event_id):
    return

def signup(request):
    return

def user_login(request):
    return

#@login_required
def user_logout(request):
    return

#@login_required
def event_signup(request, event_id):
    return

#@login_required
def add_comment(request, event_id):
    return

#@login_required
def enable_notifications(request, event_id):
    return

def organiser_login(request):
    return

#@login_required
def add_event(request):
    return

#def edit_event(request, event_id): ??

#@login_required
def delete_event(request, event_id):
    return

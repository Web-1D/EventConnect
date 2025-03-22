from django.urls import path
from webapp import views

app_name = 'webapp'

urlpatterns = [
    # Public Views
    path('', views.home, name='home'),
    path('contact-us/', views.contact, name='contact'),
    path('q&a/', views.qa, name='qa'),

    # User Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Event Categories
    path('categories/<str:category_name>/', views.categories, name='categories'),
    path('organiser_account/add-category/', views.add_category, name='add_category'),

    # Event Details and Comments
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/comments/', views.event_comments, name='event_comments'),
    path('event/<int:event_id>/sign-up/', views.event_signup, name='event_signup'),
    path('event/<int:event_id>/enable-notifications/', views.enable_notifications, name='enable_notifications'),
    path('ajax/search-events/', views.ajax_search_events, name='search_events'),
    path('search-event/', views.search_event_redirect, name='search_event_redirect'),
    path('autocomplete/', views.autocomplete_events, name='autocomplete_events'),


    # Organiser Views
    path('organiser_account/', views.organiser_account, name='organiser_account'),
    path('organiser_account/add-event/<category_name>/', views.add_event, name='add_event'),
    path('organiser_account/edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('organiser_account/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),


    path('ajax/search-events/', views.search_events, name='search_events')


]
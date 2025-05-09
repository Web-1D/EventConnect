from django.urls import path
from webapp import views

app_name = 'webapp'

urlpatterns = [
    # Public Views
    path('', views.home, name='home'),
    path('contact-us/', views.contact, name='contact'),
    path('q&a/', views.qa, name='qa'),
    path('q&a/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('q&a/delete/<int:message_id>/', views.delete_message, name='delete_message'),

    # User Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Event Categories
    path('categories/<str:category_name>/', views.categories, name='categories'),

    # Event Details and Actions
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/comments/', views.event_comments, name='event_comments'),
    path('event/<int:event_id>/sign-up/', views.event_signup, name='event_signup'),
    path('event/<int:event_id>/enable-notifications/', views.enable_notifications, name='enable_notifications'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('event/<int:event_id>/unregister/', views.unregister_event, name='unregister_event'),
    path('more-events/', views.more_events, name='more_events'),


    # Search and Autocomplete
    path('ajax/search-events/', views.search_events, name='search_events'),
    path('search-event/', views.search_event_redirect, name='search_event_redirect'),
    path('autocomplete/', views.autocomplete_events, name='autocomplete_events'),

    # User-Specific Views
    path('my-events/', views.my_events, name='my_events'),
    path('notifications/', views.notifications_view, name='notifications'),

    # Organiser Views
    path('organiser_account/', views.organiser_account, name='organiser_account'),
    path('organiser_account/add-event/<category_name>/', views.add_event, name='add_event'),
    path('organiser_account/edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('organiser_account/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
]

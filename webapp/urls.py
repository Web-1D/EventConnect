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
    path('user-login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),

    # Event Categories
    path('categories/<str:category_name>/', views.categories, name='categories'),

    # Event Details and Comments
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/comments/', views.event_comments, name='event_comments'),
    path('event/<int:event_id>/sign-up/', views.event_signup, name='event_signup'),
    path('event/<int:event_id>/enable-notifications/', views.enable_notifications, name='enable_notifications'),

    # Organiser Views
    path('organiser-login/', views.organiser_login, name='organiser_login'),
    path('organiser-account/', views.organiser_account, name='organiser_account'),
    path('organiser-account/add-event/', views.add_event, name='add_event'),
    path('organiser-account/edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('organiser-account/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
]
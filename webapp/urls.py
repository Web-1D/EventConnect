from django.urls import path
from webapp import views

app_name = 'webapp'

urlpatterns = [
    # Public Views
    path('', views.home, name='home'),
    path('contact-us/', views.contact, name='contact'),
    path('q&a/', views.qa, name='qa'),

]

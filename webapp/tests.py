from django.test import TestCase
from webapp.models import User, Category, Event, Comment, QAForum
from webapp.forms import CategoryForm, UserForm, EventForm
from django.utils import timezone
from django.urls import reverse

class ModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sean", email="sean@test.com", password="test123", role="user")
        self.category = Category.objects.create(name="Music")

        self.organiser = User.objects.create_user(username="organiser1", email="organiser1@test.com", password="organ123", role="organiser")
        self.event = Event.objects.create(
            title="Glasgow Rock Club Concert",
            description="A night of rocking and rolling for all students",
            date=timezone.now(),
            location="Kelvingrove Bandstand",
            category=self.category,
            organiser=self.organiser
        )

        self.comment = Comment.objects.create(user=self.user, event=self.event, comment="Bet they'll sound amazing!")
        self.qa = QAForum.objects.create(user=self.user, message_text="Login not working?", timestamp=timezone.now())

    def test_create_user(self):
        self.assertEqual(self.user.username, "sean")
        self.assertEqual(self.user.email, "sean@test.com")
        self.assertTrue(self.user.check_password("test123"))
        self.assertEqual(self.user.role, "user")

    def test_create_category(self):
        self.assertEqual(self.category.name, "Music")

    def test_create_event(self):
        self.assertEqual(self.event.title, "Glasgow Rock Club Concert")
        self.assertEqual(self.event.category.name, "Music")
        self.assertEqual(self.event.organiser.username, "organiser1")
    
    def test_create_comment(self):
        self.assertEqual(self.comment.comment, "Bet they'll sound amazing!")
        self.assertEqual(self.comment.user.username, "sean")
    
    def test_create_qa(self):
        self.assertEqual(self.qa.message_text, "Login not working?")
        self.assertEqual(self.qa.user.username, "sean")

class ViewsTestsNoData(TestCase):
    def test_home_view_with_no_events(self):
        response = self.client.get(reverse('webapp:home'))

        # 200 means a successful request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No popular events found.")
        self.assertContains(response, "No recent events found.")

    def test_category_view_with_no_events(self):
        add_category('Sport')
        
        response = self.client.get(reverse('webapp:categories', args=['Sport']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No events found in this category.")
        self.assertTemplateUsed(response, 'webapp/category.html')

class ViewsTestsWithData(TestCase):  
    def setUp(self):
        self.user = User.objects.create_user(username="sean", email="sean@test.com", password="test123", role="user")
        self.organiser = User.objects.create_user(username="organiser2", email="organiser2@test.com", password="organ23", role="organiser")
        self.category = Category.objects.create(name="Sport")
        self.event = Event.objects.create(
            title="Tennis Tournament", description="Fun tourny",
            date=timezone.now(), location="Garscube",
            category=self.category, organiser=self.organiser
        )
        self.comment = Comment.objects.create(user=self.user, event=self.event, comment="I'm going to win!!!")

    def test_home_view(self):
        response = self.client.get(reverse('webapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sport")
        self.assertContains(response, "Tennis Tournament")
        self.assertTemplateUsed(response, 'webapp/home.html')
    
    def test_contact_view(self):
        response = self.client.get(reverse('webapp:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/contact.html')
    
    def test_contact_view_post(self):
        response = self.client.post(reverse('webapp:contact'), {
            'name': 'Test User',
            'email': 'user@test.com',
            'message': 'Need help with my account'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message_sent' in response.context)
    
    def test_event_view(self):
        response = self.client.get(reverse('webapp:event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/event.html')
        self.assertContains(response, self.event.title)
    
    def test_signup_view(self):
        response = self.client.get(reverse('webapp:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/signup.html')
    
    def test_user_login_view_invalid(self):
        response = self.client.post(reverse('webapp:user_login'), {'username': 'test', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid login details supplied.")

    def test_event_signup_view_authenticated(self):
        self.client.login(username='sean', password='test123')
        response = self.client.post(reverse('webapp:event_signup', args=[self.event.id]))
        # 302 redirects after a successful signup
        self.assertEqual(response.status_code, 302)
    
    def test_add_comment_view_authenticated(self):
        self.client.login(username='sean', password='test123')
        response = self.client.post(reverse('webapp:add_comment', args=[self.event.id]), {'comment': 'Cant wait!'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(comment='Cant wait!').exists())
    
    def test_organiser_account_view(self):
        self.client.login(username='organiser2', password='organ23')
        response = self.client.get(reverse('webapp:organiser_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/organiser_account.html')

class FormsTests(TestCase):
    def test_user_form_valid_input(self):
        form_data = {'username': 'test', 'email': 'test@test.com', 'password': 'password', 'role': 'user'}
        form = UserForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
    
    def test_user_form_invalid_input(self):
        form_data = {'username': '', 'email': '', 'password': 'password', 'role': 'user'}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_category_form_valid_input(self):
        form_data = {'name': 'Music'}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid_input(self):
        form_data = {'name': ''}
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def setUp(self):
        self.category = Category.objects.create(name='Music')

    def test_event_form_valid_input(self):
        form_data = {
            'title': 'Rock Concert',
            'description': 'A fun night of rock music',
            'date': timezone.now(),
            'location': 'Kelvingrove Bandstand',
            'category': self.category.id,
            'event_image': None
        }

        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid_input_missing_field(self):
        form_data = {
            'title': '',
            'description': 'A fun night of rock music',
            'date': timezone.now(),
            'location': 'Kelvingrove Bandstand',
            'category': self.category.id
        }

        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

        # title is required so should be in error message
        self.assertIn('title', form.errors)

    def test_event_form_invalid_input_invalid_date(self):
        form_data = {
            'title': 'Rock Concert',
            'description': 'A fun night of rock music',
            'date': 'invalid date',
            'location': 'Kelvingrove Bandstand',
            'category': self.category.id
        }

        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

        # checking date validation
        self.assertIn('date', form.errors) 

class URLsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sean", email="sean@test.com", password="test123", role="user")
        self.organiser = User.objects.create_user(username="organiser2", email="organiser2@test.com", password="organ23", role="organiser")
        self.category = Category.objects.create(name="Sport")

        self.event = Event.objects.create(
            title="Tennis Tournament", description="Fun tourny",
            date=timezone.now(), location="Garscube",
            category=self.category, organiser=self.organiser
        )
        self.comment = Comment.objects.create(user=self.user, event=self.event, comment="I'm going to win!!!")

        # Login a user and organiser
        self.client.login(username="sean", password="test123")
        self.client.login(username="organiser2", password="organ23")  

    def test_home_url(self):
        url = reverse('webapp:home')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_contact_url(self):
        url = reverse('webapp:contact')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_qa_url(self):
        url = reverse('webapp:qa')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_signup_url(self):
        url = reverse('webapp:signup')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_user_login_url(self):
        url = reverse('webapp:user_login')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_logout_url(self):
        url = reverse('webapp:logout')
        response = self.client.get(url)

        # Should Redirect after logging out
        self.assertEqual(response.status_code, 302)
    
    def test_categories_url(self):
        url = reverse('webapp:categories', args=['Sport'])
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)

    def test_event_url(self):
        url = reverse('webapp:event', args=[self.event.id])
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_event_signup_url(self):
        url = reverse('webapp:event_signup', args=[self.event.id])
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)

    """
    // no template for this yet
    def test_enable_notifications_url(self):
        # Assuming an event with ID 1 exists
        self.client.login(username='sean', password='test123')
        url = reverse('webapp:enable_notifications', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    """

    def test_add_comment_url(self):
        url = reverse('webapp:add_comment', args=[self.event.id])
        response = self.client.get(url)

        # Should redirect back to event after adding a comment
        self.assertEqual(response.status_code, 302)

    def test_organiser_login_url(self):
        url = reverse('webapp:organiser_login')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)

    def test_organiser_account_url(self):
        url = reverse('webapp:organiser_account')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_add_event_url(self):
        url = reverse('webapp:add_event')
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)

    # Missing edit event template
    def test_edit_event_url(self):
        url = reverse('webapp:edit_event', args=[self.event.id])
        response = self.client.get(url)

        # No need to redirect
        self.assertEqual(response.status_code, 200)
    
    def test_delete_event_url(self):
        url = reverse('webapp:delete_event', args=[self.event.id])
        response = self.client.get(url)

        # Should redirect after event is deleted
        self.assertEqual(response.status_code, 302)

def add_category(name):
        category = Category.objects.get_or_create(name=name)[0]
        category.save()
        return category
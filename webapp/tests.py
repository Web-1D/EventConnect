from django.test import TestCase
from webapp.models import User, Category, Event, Comment, QAForum
from django.utils import timezone
from django.urls import reverse

class ModelTest(TestCase):
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

class ViewsTestNoData(TestCase):
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

class ViewsTestWithData(TestCase):  
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

def add_category(name):
        category = Category.objects.get_or_create(name=name)[0]
        category.save()
        return category
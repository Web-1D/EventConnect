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

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sean", email="sean@test.com", password="test123", role="user")
        self.organiser = User.objects.create_user(username="organiser2", email="organiser2@test.com", password="organ23", role="organiser")
        self.category = Category.objects.create(name="Sport")
        self.event = Event.objects.create(
            title="Tennis Tournament", description="Fun tourny",
            date=timezone.now(), location="Garscube",
            category=self.category, organiser=self.organiser
        )

    def test_home_view(self):
        response = self.client.get(reverse('webapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sport")
        self.assertContains(response, "Tennis Tournament")
        self.assertTemplateUsed(response, 'webapp/home.html')

    
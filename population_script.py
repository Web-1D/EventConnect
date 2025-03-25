import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventConnect.settings')
django.setup()

from webapp.models import Category, Event, Comment, QAForum, User
from django.conf import settings


User.objects.all().delete()
Category.objects.all().delete()
Event.objects.all().delete()
Comment.objects.all().delete()
QAForum.objects.all().delete()

def populate():
    # Create Users
    organiser = User.objects.create_user(username="sean", email="sean@example.com", password="test123", role="organiser")
    user1 = User.objects.create_user(username="sinead", email="sinead@example.com", password="test123", role="user")
    user2 = User.objects.create_user(username="costi", email="costi@example.com", password="test123", role="user")

    # Create Categories
    sport_category = Category.objects.create(name="Sport")
    music_category = Category.objects.create(name="Music")
    academic_category = Category.objects.create(name="Academic")
    cultural_category = Category.objects.create(name="Cultural")
    more_category = Category.objects.create(name="More")

    # Create Events
    event1 = Event.objects.create(
        title="University Football Championship",
        description="Annual university football tournament.",
        date=datetime(2025, 10, 10, 16, 0),
        location="Garscube",
        category=sport_category,
        organiser=organiser,
        event_image="event_images/football.jpg"
    )

    event2 = Event.objects.create(
        title="Jazz Night",
        description="A night of jazz performances.",
        date=datetime(2025, 6, 25, 19, 30),
        location="QMU",
        category=music_category,
        organiser=organiser,
        event_image="event_images/jazz.jpg"
    )

    event3 = Event.objects.create(
        title="Mathematics Workshop",
        description="A workshop on advanced calculus.",
        date=datetime(2025, 4, 5, 10, 00),
        location="Science Building, Room 203",
        category=academic_category,
        organiser=organiser,
        event_image="event_images/maths.jpg"
    )

    event4 = Event.objects.create(
        title="Cultural Festival",
        description="A celebration of diverse cultures through music, dance, and food.",
        date=datetime(2025, 5, 15, 12, 0),
        location="Kelvingrove",
        category=cultural_category,
        organiser=organiser,
        event_image="event_images/culture.jpg"
    )

    event5 = Event.objects.create(
        title="GameJam",
        description="A fun day for code lovers to compete.",
        date=datetime(2025, 5, 10, 14, 0),
        location="Boyd Orr",
        category=more_category,
        organiser=organiser,
        event_image="event_images/gamejam.jpg"
    )

    event1.attendees.add(user1, user2)
    event2.attendees.add(user1, user2)
    event3.attendees.add(user2)
    event4.attendees.add(user1, user2)
    event5.attendees.add(user2)

    # Create Comments
    Comment.objects.create(user=user1, event=event1, comment="Excited for the match!")
    Comment.objects.create(user=user2, event=event2, comment="Love jazz music!")
    Comment.objects.create(user=user1, event=event3, comment="Hope to learn something new!")
    Comment.objects.create(user=user2, event=event4, comment="Looking forward to experiencing different cultures.")
    Comment.objects.create(user=user1, event=event5, comment="Great opportunity to work as a team!")

    # Create QAForum Messages
    QAForum.objects.create(user=user1, message_text="How do I participate in the football championship?")
    QAForum.objects.create(user=user2, message_text="Are there any free tickets for Jazz Night?")
    QAForum.objects.create(user=user1, message_text="Will the Mathematics Workshop include a Q&A session?")
    QAForum.objects.create(user=user2, message_text="What kind of food will be available at the Cultural Festival?")
    QAForum.objects.create(user=user1, message_text="Can I create my own team?")

    print("Database populated successfully with Sport, Music, Academic, Cultural, and More categories.")

if __name__ == '__main__':
    populate()


import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventConnect.settings')
django.setup()

from webapp.models import User, Category, Event

def populate():
    # Clear existing data (opțional, doar pentru teste)
    Event.objects.all().delete()
    User.objects.filter(username__startswith="testuser").delete()
    User.objects.filter(username__startswith="organiser").delete()

    # Create categories if not already
    category_names = ["Sports", "Music", "Academic", "Cultural", "More"]
    categories = []
    for name in category_names:
        category, _ = Category.objects.get_or_create(name=name)
        categories.append(category)

    # Create organisers
    organisers = []
    for i in range(1, 4):
        user = User.objects.create_user(
            username=f"organiser{i}",
            password="organiserpass",
            email=f"organiser{i}@test.com",
            role="organiser"
        )
        organisers.append(user)

    # Create normal users
    for i in range(1, 6):
        User.objects.create_user(
            username=f"testuser{i}",
            password="testpass",
            email=f"user{i}@test.com",
            role="user"
        )

    # Google Maps Embed Link
    gmaps_link = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5836.714949869367!2d-4.292463482603151!3d55.86880718879993!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d20af469b3%3A0xa3f0620b655e4983!2sUniversitatea%20din%20Glasgow!5e1!3m2!1sro!2suk!4v1742891391229!5m2!1sro!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""

    # Create 3 events per category
    for category in categories:
        for i in range(1, 4):
            Event.objects.create(
                title=f"{category.name} Event {i}",
                description=f"Sample description for {category.name} Event {i}.",
                date=datetime.now() + timedelta(days=random.randint(1, 20)),
                location="University of Glasgow",
                google_maps_link=gmaps_link,
                organiser=random.choice(organisers),
                category=category
            )

    print("✅ Database populated successfully.")

if __name__ == '__main__':
    populate()
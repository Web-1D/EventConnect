import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventConnect.settings')
django.setup()

from webapp.models import User, Category, Event

def populate():

    User.objects.all().delete()
    Category.objects.all().delete()
    Event.objects.all().delete()

    # Create categories
    sports_category = Category.objects.create(name="Sports")
    music_category = Category.objects.create(name="Music")
    academic_category = Category.objects.create(name="Academic")
    cultural_category = Category.objects.create(name="Cultural")
    more_category = Category.objects.create(name="More")


    # Create organisers
    organiser1 = User.objects.create_user(username="sean", email="sean@example.com", password="test123", role="organiser")
    organiser2 = User.objects.create_user(username="sinead", email="sinead@example.com", password="test123", role="organiser")
    organiser3 = User.objects.create_user(username="daniel", email="daniel@example.com", password="test123", role="organiser")


    # Create normal users
    user1 = User.objects.create_user(username="costi", email="costi@example.com", password="test123", role="user")
    user2 = User.objects.create_user(username="tanvika", email="tanvika@example.com", password="test123", role="user")

    # Google Maps Embed Links
    gmaps_garscube = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4473.387590807979!2d-4.318364316629771!3d55.902669570848374!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845a06a45d773%3A0x242b6969206f81cb!2sGarscube%20Sports%20Complex!5e0!3m2!1sen!2suk!4v1743095839049!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_stevenson = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2892.828813602485!2d-4.285869337522604!3d55.87272128284913!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845cd61545955%3A0xc8fcf2b652b4fd5a!2sStevenson%20Building%2C%2077%20Oakfield%20Ave%2C%20Glasgow%20G12%208LT!5e0!3m2!1sen!2suk!4v1743096105749!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_qmu = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.3699996551773!2d-4.291395499999997!3d55.873596199999994!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845ce12aef097%3A0xe9f1db5b4c772ef!2sQueen%20Margaret%20Union!5e0!3m2!1sen!2suk!4v1743096205440!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_chapel = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.4869702074902!2d-4.2895274999999895!3d55.871567!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d21ba12c8d%3A0x32b2b57eb58e2ab!2sUniversity%20Chapel!5e0!3m2!1sen!2suk!4v1743096299393!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_maths = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.4270038395325!2d-4.294484300000052!3d55.872607299999984!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845cfd066d839%3A0xeab86bed8f92f0d0!2sSchool%20of%20Mathematics%20and%20Statistics!5e0!3m2!1sen!2suk!4v1743096563618!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_kelvbuild = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.471256704001!2d-4.291647000000012!3d55.87183959999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48884596fcfe844b%3A0x83d9871dfac8a5c3!2sKelvin%20Building!5e0!3m2!1sen!2suk!4v1743100270865!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_kelvpark = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.6252134212345!2d-4.283389599999992!3d55.86916869999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d3252afce9%3A0x9ef923bf94072089!2sKelvingrove%20Park!5e0!3m2!1sen!2suk!4v1743096919679!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_kelvhotel = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.800042266781!2d-4.285721300000008!3d55.86613560000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d489c2075d%3A0x173d1b7141ef927!2sKelvingrove%20Hotel%20-%20Book%20Direct%20for%20Best%20Rates.%20We&#39;re%20cheaper%20than%20online%20travel%20agents.!5e0!3m2!1sen!2suk!4v1743096959396!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_jms = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.394469628919!2d-4.2924767!3d55.8731717!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48884574f0008a73%3A0x5bfb31eedc4517b5!2sJames%20McCune%20Smith%20Learning%20Hub!5e0!3m2!1sen!2suk!4v1743099666530!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_boyd = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.37186156798!2d-4.292643299999999!3d55.87356390000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845ce39231b11%3A0xce4a79eafb2376a6!2sBoyd%20Orr%20Building!5e0!3m2!1sen!2suk!4v1743100641955!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_main = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.492525184611!2d-4.29068527734363!3d55.87147063128955!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d2136e869f%3A0x1f4cdacdefe01c76!2sMain%20Building%2C%20Glasgow%20G12%208QQ!5e0!3m2!1sen!2suk!4v1743101221137!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""

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

    print("Database populated successfully.")

if __name__ == '__main__':
    populate()
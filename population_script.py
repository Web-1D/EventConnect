import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventConnect.settings')
django.setup()

from webapp.models import User, Category, Event, Comment

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
    gmaps_guu = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d8952.480788557328!2d-4.291242800000047!3d55.8779296!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845cdf92cdf2d%3A0xd14847c3d4ae5e0a!2sGlasgow%20University%20Union!5e0!3m2!1sen!2suk!4v1743106279190!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_jms = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.394469628919!2d-4.2924767!3d55.8731717!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48884574f0008a73%3A0x5bfb31eedc4517b5!2sJames%20McCune%20Smith%20Learning%20Hub!5e0!3m2!1sen!2suk!4v1743099666530!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_boyd = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.37186156798!2d-4.292643299999999!3d55.87356390000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845ce39231b11%3A0xce4a79eafb2376a6!2sBoyd%20Orr%20Building!5e0!3m2!1sen!2suk!4v1743100641955!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""
    gmaps_main = """https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2238.492525184611!2d-4.29068527734363!3d55.87147063128955!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x488845d2136e869f%3A0x1f4cdacdefe01c76!2sMain%20Building%2C%20Glasgow%20G12%208QQ!5e0!3m2!1sen!2suk!4v1743101221137!5m2!1sen!2suk" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>"""

    # Sport events
    event1 = Event.objects.create(
        title="University Football Championship",
        description="Annual university football tournament.",
        date=datetime(2025, 10, 10, 16, 0),
        location="Garscube Sports Complex",
        category=sports_category,
        google_maps_link=gmaps_garscube,
        organiser=organiser2,
        event_image="event_images/football.jpg"
    )

    event2 = Event.objects.create(
        title="University Woman's Rugby League Trophy",
        description="Finals of the University Rugby League.",
        date=datetime(2025, 10, 2, 16, 0),
        location="Garscube Sports Complex",
        category=sports_category,
        google_maps_link=gmaps_garscube,
        organiser=organiser1,
        event_image="event_images/rugby.jpg"
    )

    event3 = Event.objects.create(
        title="University Netball Finals",
        description="Finals of the university netball tournament.",
        date=datetime(2025, 11, 14, 15, 0),
        location="Stevenson Building",
        category=sports_category,
        google_maps_link=gmaps_stevenson,
        organiser=organiser1,
        event_image="event_images/netball.jpg"
    )

    # Music events
    event4 = Event.objects.create(
        title="Jazz Night",
        description="A night of jazz performances.",
        date=datetime(2025, 6, 25, 19, 30),
        location="QMU",
        category=music_category,
        google_maps_link=gmaps_qmu,
        organiser=organiser3,
        event_image="event_images/jazz.jpg"
    )

    event5 = Event.objects.create(
        title="Open Mic Night",
        description="Bring your instrument and perform!",
        date=datetime(2025, 5, 24, 19, 0),
        location="QMU",
        category=music_category,
        google_maps_link=gmaps_qmu,
        organiser=organiser3,
        event_image="event_images/mic.jpg"
    )

    event6 = Event.objects.create(
        title="Choir Summer Performance",
        description="The University Choir's annual summer performance.",
        date=datetime(2025, 6, 28, 19, 0),
        location="University Chapel",
        category=music_category,
        google_maps_link=gmaps_chapel,
        organiser=organiser2,
        event_image="event_images/choir.jpg"
    )

    # Academic events
    event7 = Event.objects.create(
        title="Mathematics Workshop",
        description="A workshop on advanced calculus.",
        date=datetime(2025, 4, 5, 10, 0),
        location="Room 203, Maths and Stats Building",
        category=academic_category,
        google_maps_link=gmaps_maths,
        organiser=organiser2,
        event_image="event_images/maths.jpg"
    )

    event8 = Event.objects.create(
        title="Physics Society Meetup",
        description="Join us for discussion and pizza!",
        date=datetime(2025, 4, 10, 18, 30),
        location="Room 423, Kelvin Building",
        category=academic_category,
        google_maps_link=gmaps_kelvbuild,
        organiser=organiser3,
        event_image="event_images/physics.jpg"
    )

    event9 = Event.objects.create(
        title="Philosophy Society Meetup",
        description="A gathering of the philosophy society.",
        date=datetime(2025, 4, 2, 19, 0),
        location="QMU",
        category=academic_category,
        google_maps_link=gmaps_qmu,
        organiser=organiser3,
        event_image="event_images/philosphy.jpg"
    )

    # Cultural events
    event10 = Event.objects.create(
        title="Cultural Festival",
        description="A celebration of diverse cultures through music, dance, and food.",
        date=datetime(2025, 5, 15, 12, 0),
        location="Kelvingrove Park",
        category=cultural_category,
        google_maps_link=gmaps_kelvpark,
        organiser=organiser2,
        event_image="event_images/culture.jpg"
    )

    event11 = Event.objects.create(
        title="Gaelic Society Ball",
        description="The Gaelic Society's Annual Ball.",
        date=datetime(2025, 5, 10, 19, 0),
        location="Glasgow University Union",
        category=cultural_category,
        google_maps_link=gmaps_guu,
        organiser=organiser2,
        event_image="event_images/gaelic.jpg"
    )

    event12 = Event.objects.create(
        title="Germany Society Film Viewing",
        description="Watch a German film with free snacks.",
        date=datetime(2025, 4, 5, 18, 30),
        location="Room 408, JMS",
        category=cultural_category,
        google_maps_link=gmaps_jms,
        organiser=organiser1,
        event_image="event_images/german.jpg"
    )

    event13 = Event.objects.create(
        title="GameJam",
        description="A fun day for code lovers to compete.",
        date=datetime(2025, 5, 10, 14, 0),
        location="706 Lab, Boyd Orr",
        category=more_category,
        google_maps_link=gmaps_boyd,
        organiser=organiser3,
        event_image="event_images/gamejam.jpg"
    )

    event14 = Event.objects.create(
        title="Volunteers Fair",
        description="Meet organisations and find a volunteer placement.",
        date=datetime(2025, 10, 5, 11, 0),
        location="University Main Building",
        category=more_category,
        google_maps_link=gmaps_main,
        organiser=organiser2,
        event_image="event_images/volunteer.jpg"
    )

    event15 = Event.objects.create(
        title="Climate Change Talk",
        description="An afternoon with climate experts.",
        date=datetime(2025, 9, 23, 14, 30),
        location="Room 602, JMS",
        category=more_category,
        google_maps_link=gmaps_jms,
        organiser=organiser1,
        event_image="event_images/climate.jpg"
    )

    event3.attendees.add(user1, user2)
    event5.attendees.add(user1)
    event7.attendees.add(user1, user2)
    event9.attendees.add(user2)

    Comment.objects.create(user=user1, event=event1, comment="Excited for the matches!")
    Comment.objects.create(user=user2, event=event2, comment="Love a bit of rugby!")
    Comment.objects.create(user=user1, event=event3, comment="Im going to beat everyone")
    Comment.objects.create(user=user2, event=event4, comment="Hopefully they have a saxophone?!")
    Comment.objects.create(user=user1, event=event5, comment="Ive got the best voice ever")


    print("Database populated successfully.")

if __name__ == '__main__':
    populate()
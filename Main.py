from PIL import Image
from random import randint
from Google import get_list, get_appointments, get_birthdays
from Snippets import create_date, create_birthdays, create_news, create_appointments, stitch_images, create_error, create_dog, create_picture
from Data import get_date, get_news, get_dog, get_picture


def create_daily():

    birthday_cal = "422aed951e577227681ab482cbc171bb278be3e292971fe0e7bda901c32ce43f@group.calendar.google.com"

    date_snippet = create_date(get_date())

    birthdays = get_birthdays(birthday_cal)
    birthday_snippet = create_birthdays(birthdays) if birthdays else None

    appointments = get_appointments()
    appointment_snippet = create_appointments(appointments) if appointments else None

    news_items = get_news()
    news_snippet = create_news(news_items) if news_items else create_error("Unable to load news")

    dog = get_dog()
    dog_snippet = create_dog(dog) if dog else create_error("Unable to load dog")

    picture = get_picture()
    picture_snippet = create_picture(picture) if picture else create_error("Unable to load picture")

    stitch_images([date_snippet, birthday_snippet, appointment_snippet, news_snippet, dog_snippet, picture_snippet])


create_daily()

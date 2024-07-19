from random import randint
from Google import get_list, get_appointments, get_birthdays
from Snippets import create_date, create_birthdays, create_news, create_appointments, stitch_images, create_error, create_dog, create_picture, create_quote, create_history, create_joke, create_fact, create_list
from Data import get_date, get_news, get_dog, get_picture, get_quote, get_history, get_joke, get_fact


def create_daily():

    birthday_cal = "422aed951e577227681ab482cbc171bb278be3e292971fe0e7bda901c32ce43f@group.calendar.google.com"

    date_snippet = create_date(get_date())

    birthdays = get_birthdays(birthday_cal)
    birthday_snippet = create_birthdays(birthdays) if birthdays else None

    appointments = get_appointments()
    appointment_snippet = create_appointments(appointments) if appointments else None

    news_items = get_news()
    news_snippet = create_news(news_items) if news_items else create_error("Unable to load news")

    triv_i = randint(0, 5)

    if triv_i == 0:
        dog = get_dog()
        trivia_snippet = create_dog(dog) if dog else create_error("Unable to load \"dog of the day\"")

    elif triv_i == 1:
        picture = get_picture()
        trivia_snippet = create_picture(picture) if picture else create_error("Unable to load \"picture of the day\"")

    elif triv_i == 2:
        quote = get_quote()
        trivia_snippet = create_quote(quote) if quote else create_error("Unable to load \"quote of the day\"")

    elif triv_i == 3:
        history = get_history()
        trivia_snippet = create_history(history) if history else create_error("Unable to load \"history of the day\"")

    elif triv_i == 4:
        joke = get_joke()
        trivia_snippet = create_joke(joke) if joke else create_error("Unable to load \"joke of the day\"")

    elif triv_i == 5:
        fact = get_fact()
        trivia_snippet = create_fact(fact) if fact else create_error("Unable to load \"fact of the day \"")

    return stitch_images([date_snippet, birthday_snippet, appointment_snippet, news_snippet, trivia_snippet])


def list():
    return create_list(get_list("UHhMeHVYX2dhaGZWdGJ2ag"), "Boodschappen")


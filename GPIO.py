from gpiozero import Button
from Prints import print_daily, print_list
from time import sleep


def gpio():

    daily_button = Button(2)
    list_button = Button(3)
    calendar_button = Button(4)

    while True:

        if daily_button.is_pressed:
            print_daily()
            sleep(2)

        if list_button.is_pressed:
            print_list()
            sleep(2)

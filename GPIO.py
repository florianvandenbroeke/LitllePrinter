from gpiozero import Button
from Prints import create_daily, create_tasklist, print_item
from time import sleep

daily_button = Button(2)
list_button = Button(3)
calendar_button = Button(4)


def gpio():
    while True:

        if daily_button.is_pressed:
            print_item(create_daily())
            sleep(2)

        if list_button.is_pressed:
            print_item(create_tasklist())
            sleep(2)

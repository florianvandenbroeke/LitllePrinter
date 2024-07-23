from gpiozero import Button
from Prints import print_daily, print_list
from time import sleep
from signal import pause

daily_button = Button(2)
list_button = Button(3)
calendar_button = Button(4)


# def gpio():
#     while True:
#
#         if daily_button.is_pressed:
#             print_daily()
#             sleep(2)
#
#         if list_button.is_pressed:
#             print_list()
#             sleep(2)

def gpio():
    daily_button.when_pressed = print_daily
    list_button.when_pressed = print_list

    pause()

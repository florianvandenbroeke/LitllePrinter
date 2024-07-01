from Graphics import Frame
from PIL import Image
import datetime as dt

clab = "Clab.otf"
clab_bold = "Clab bold.otf"
franchise = "Franchise.ttf"
futura = "futura medium bt.ttf"
payfair = "Payfair.ttf"
paper = "Paper Banner.ttf"
party = "Party.ttf"
product = "Product Sans Regular.ttf"
product_bold = "Product Sans Bold.ttf"
times = "Times New Roman.ttf"
market_deco = "market deco.ttf"
dillan = "Dillan.otf"


def create_date(dayword, day, month, h, m):
    frame = Frame()

    frame.add_whitespace(25)
    frame.draw_width(dayword, franchise, 320)
    frame.add_whitespace(15)
    frame.draw_width(f"{day} {month} | {h}:{m}", futura, 320)
    frame.add_whitespace(10)

    return frame.show()


def create_quote(quote, author):
    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/quote_header.png")
    frame.add_whitespace(20)
    frame.text_wrap(f"\"{quote}\"", payfair, 28, 300, spacing=1)
    frame.add_whitespace(10)
    frame.text_wrap(f"- {author}", product, 20, 100, alignment="r", offset=15)
    frame.add_whitespace(20)

    return frame.show()


def create_news(items):
    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/news_header.png")
    frame.add_whitespace(20)

    for i in range(3):
        frame.text_wrap(items[i], clab, 20, 350, "r" * (i % 2) + "l" * (not i % 2), 15, spacing=4)
        frame.add_whitespace(16)

    return frame.show()


def create_birthdays(birhdays):

    frame = Frame()

    frame.add_whitespace(5)
    frame.draw_center_text("[BIRTHDAYS]", paper, 46)
    frame.add_whitespace(10)

    for name in birhdays:
        frame.text_wrap(name, party, 45, 200)
        frame.add_whitespace(10)

    return frame.show()


def create_dog(dog):

    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/dog_header.png")
    frame.add_whitespace(20)
    frame.center_paste(dog, 280, border=3)
    frame.add_whitespace(15)

    return frame.show()


def create_picture(pic, pic_desc):

    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/picture_header.png")
    frame.add_whitespace(20)
    frame.center_paste(pic, 384)
    frame.add_whitespace(15)
    frame.text_wrap(pic_desc, futura, 15, 300, spacing=1)
    frame.add_whitespace(15)

    return frame.show()


def create_history(title, year):

    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/history_header.png")
    frame.add_whitespace(20)
    frame.text_wrap(str(year), market_deco, 50, 300, alignment="c", offset=0)
    frame.add_whitespace(5)
    swash = Image.open("Images/swash.png")
    frame.center_paste(swash, width=70)
    frame.add_whitespace(10)
    frame.text_wrap(title, times, 20, 360, alignment="c", offset=0)
    frame.add_whitespace(15)

    return frame.show()


def create_joke(joke):

    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/joke_header.png")
    frame.add_whitespace(15)
    frame.text_wrap(joke, dillan, 25, 300)
    frame.add_whitespace(15)

    return frame.show()


def create_fact(fact):

    frame = Frame()

    frame.paste_im("Images/dot_line.png")
    frame.add_whitespace(20)
    frame.paste_im("Images/fact_header.png")
    frame.add_whitespace(8)

    bulb = Image.open("Images/bulb.png")
    frame.center_paste(bulb, 60)
    frame.add_whitespace(10)

    frame.text_wrap(fact, product, 22, 350)
    frame.add_whitespace(10)

    return frame.show()


def create_appointments(appointments):

    frame = Frame()
    frame.add_whitespace(0)

    for appointment in appointments:

        title, start_time, end_time = appointment

        if start_time:
            start_time = dt.datetime.fromisoformat(start_time).strftime("%H:%M")
            end_time = dt.datetime.fromisoformat(end_time).strftime("%H:%M")

            start_h = frame.current_h
            frame.text_wrap(f"{start_time} - {end_time}", product_bold, 20, 350, alignment="l", offset=10)
            frame.add_whitespace(5)
            frame.text_wrap(title, product, 22, 350, alignment="l", offset=10)
            end_h = frame.current_h
            frame.draw_line((5, start_h, 5, end_h), 2)
            frame.add_whitespace(8)

        else:
            frame.text_wrap(title, product_bold, 22, 350, alignment="l", offset=7)
            frame.add_whitespace(8)

    return frame.show()


def create_list(items, list_name):

    frame = Frame()

    frame.add_whitespace(10)
    frame.draw_width(list_name, clab_bold, 360)
    frame.add_whitespace(5)

    if len(items):
        for item in items:
            start_h = frame.current_h
            frame.text_wrap(item, clab, 30, 360, alignment="l", offset=35)
            end_h = frame.current_h
            h = (start_h + end_h) // 2
            frame.draw_rect((12, h-8, 28, h+8), 2)
            frame.add_whitespace(12)
    else:
        frame.draw_left_text("No items on this list!", product, 25, add_offset=12)
        frame.add_whitespace(12)

    return frame.show()


def create_error(msg):

    frame = Frame()
    frame.add_whitespace(10)
    frame.text_wrap(msg, product, 20, 380)
    frame.add_whitespace(10)

    return frame.show()

from PIL import Image, ImageDraw, ImageFont
import textwrap

wagner = "NT Wagner.otf"
franchise = "Franchise.ttf"
clab = "Clab.otf"
product = "Product Sans Regular.ttf"
blackout = "Blackout Sunrise.ttf"
dillan = "Dillan.otf"
market_deco = "market deco.ttf"
harlem_deco = "harlem deco.ttf"
retrolight = "Retrolight.ttf"
london = "Old London.ttf"
linux = "Linux.ttf"


class Frame:

    def __init__(self, width=384):
        self.width = width
        self.image = Image.new("RGB", (self.width, 1000), "white")
        self.d = ImageDraw.Draw(self.image)
        self.current_h = 0
        self.boxcoords = ()

    def draw_line(self):
        self.d.line((0, self.current_h, self.width, self.current_h), width=1, fill="red")
        self.current_h += 1

    def paste_im(self, path):
        to_paste = Image.open(path)
        self.image.paste(to_paste)
        self.current_h += to_paste.height

    def add_whitespace(self, space):
        self.current_h += space

    def draw_text(self, text, font, size):
        font = ImageFont.truetype(font, size)
        offset = font.getmetrics()[1]
        self.d.text((self.width/2, self.current_h - offset), text, fill="black", font=font, align="center", spacing=4, anchor="ma")
        self.boxcoords = self.d.textbbox((self.width/2, self.current_h - offset), text, anchor="ma", font=font, align="center", spacing=4)
        self.d.rectangle(self.boxcoords, outline="black")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def text_wrap(self, text, font, size, max_width):

        # self.d.rectangle((self.width / 2 - max_width / 2, 0, self.width / 2 + max_width / 2, 1000), outline="black")

        font_t = ImageFont.truetype(font, size)
        wordlist = text.split(" ")
        line = []
        textlist = []

        for word in wordlist:

            line.append(word)
            linewidth = self.d.textbbox((0, 0), " ".join(line), font=font_t)[2]

            if linewidth > max_width:
                textlist += line[:-1]
                textlist.append("\n")
                line = [line[-1]]

        textlist += line

        if textlist[0] == "\n":
            textlist.pop(0)

        self.draw_text(" ".join(textlist), font, size)

    def draw_underline(self, offfset, w):
        x1, y1 = self.boxcoords[0], self.boxcoords[3] + offfset
        x2, y2 = self.boxcoords[2], self.boxcoords[3] + offfset
        self.d.line((x1, y1, x2, y2), "black", width=w)
        self.current_h += offfset + w

    def draw_sidebars(self, offset, w):
        x1, y1 = self.boxcoords[0] - offset, self.boxcoords[1]
        x2, y2 = self.boxcoords[2] + offset, self.boxcoords[3]
        self.d.line((x1, y1, x1, y2), fill="black", width=w)
        self.d.line((x1, (y1+y2)//2, 0, (y1+y2)//2), fill="black", width=w)
        self.d.line((x2, y1, x2, y2), fill="black", width=w)
        self.d.line((x2, (y1+y2)//2, self.width, (y1+y2)//2), fill="black", width=w)

    def show(self):
        self.image = self.image.crop((0, 0, self.width, self.current_h))
        self.image.show()


def create_date():

    front = Frame()

    front.add_whitespace(25)
    front.draw_text("JANUARI", harlem_deco, 45)
    front.draw_underline(offfset=22, w=2)
    front.add_whitespace(22)
    front.draw_text("18", market_deco, 200)
    front.add_whitespace(27)
    front.draw_text("Donderdag", franchise, 55)
    front.draw_sidebars(offset=10, w=3)
    front.add_whitespace(25)
    front.draw_text("Dit is een voorbeeld van een tekst die over meerdere ljnen moet komen", london, 50)
    front.draw_underline(offfset=3, w=2)
    front.show()

def create_quote():

    quote = "\"Het leven is een aaneenschakeling van teleurstellingen en dan ga je dood.\""

    frame = Frame()

    frame.paste_im("Images/quote_header.png")
    frame.draw_line()
    frame.add_whitespace(20)
    frame.draw_line()
    frame.text_wrap(quote, linux, 35, 300)
    frame.draw_line()
    frame.add_whitespace(35)
    frame.draw_line()

    frame.show()

create_quote()
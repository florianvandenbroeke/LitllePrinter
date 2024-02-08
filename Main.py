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


class Frame:

    def __init__(self, width=384):
        self.width = width
        self.image = Image.new("RGB", (self.width, 500), "white")
        self.d = ImageDraw.Draw(self.image)
        self.current_h = 0
        self.boxcoords = ()

    def paste_im(self, path):
        to_paste = Image.open(path)
        self.image.paste(to_paste)
        self.current_h += to_paste.height

    def add_whitespace(self, space):
        self.current_h += space

    def draw_text(self, text, font, size):
        font = ImageFont.truetype(font, size)
        self.boxcoords = self.d.textbbox((0, 0), text, font=font)
        textwidth = self.boxcoords[2] - self.boxcoords[0]
        self.d.text((self.width/2 - textwidth / 2, self.current_h), text, fill="black", font=font, align="center")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def text_wrap(self, text, font, size, max_width):

        # self.d.rectangle((self.width / 2 - max_width / 2, 0, self.width / 2 + max_width / 2, 500), outline="black")

        font_t = ImageFont.truetype(font, size)
        wordlist = text.split(" ")
        split_i = 0

        for i in range(len(wordlist)):

            linestring = " ".join(wordlist[split_i:i+1])
            boxcoords = self.d.textbbox((0, 0), linestring, font=font_t)
            textwidth = boxcoords[2] - boxcoords[0]

            if textwidth > max_width:
                wordlist.insert(i, "\n")
                split_i = i

        self.draw_text(" ".join(wordlist), font, size)



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
    frame.add_whitespace(25)
    frame.text_wrap(quote, product, 30, 270)

    frame.show()

create_quote()
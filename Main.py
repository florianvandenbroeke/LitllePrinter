from PIL import Image, ImageDraw, ImageFont

width = 384

im = Image.new("RGB", (width, 500), "white")

wagner = "NT Wagner.otf"
franchise = "Franchise.ttf"
clab = "Clab.otf"
product = "Product Sans Regular.ttf"
blackout = "Blackout Sunrise.ttf"
dillan = "Dillan.otf"
deco = "Deco.ttf"

class DateFront:

    def __init__(self, image):
        self.image = image
        self.d = ImageDraw.Draw(self.image)
        self.current_h = 0
        self.boxcoords = ()

    def add_whitespace(self, space):
        self.current_h += space

    def draw_text(self, text, font, size):
        font = ImageFont.truetype(font, size)
        self.d.text((width/2, self.current_h), text, fill="black", font=font, anchor="mt")
        self.boxcoords = self.d.textbbox((width/2, self.current_h), text, font=font, anchor="mt")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

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
        self.d.line((x2, (y1+y2)//2, width, (y1+y2)//2), fill="black", width=w)


front = DateFront(im)

front.add_whitespace(30)
front.draw_text("Mei", deco, 65)
front.draw_underline(offfset=3, w=2)
front.add_whitespace(28)
front.draw_text("16", deco, 200)
front.add_whitespace(27)
front.draw_text("Woensdag", franchise, 65)
front.draw_sidebars(offset=10, w=4)

# draw_text(im, 30, "Mei", deco, 65)
# ImageDraw.Draw(im).line((70, 100, 310, 100), fill="black", width=2)
# draw_text(im, 120, "14", deco, 200)
# draw_text(im, 300, "Zondag", franchise, 55)

im.show()
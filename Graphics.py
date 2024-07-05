from PIL import Image, ImageDraw, ImageOps, ImageFont


class Frame:

    def __init__(self, width=384):
        self.boxcoords = None
        self.width = width
        self.image = Image.new("RGB", (self.width, 1000), "white")
        self.d = ImageDraw.Draw(self.image)
        self.current_h = 0

    def draw_line(self, coords, width):
        self.d.line(coords, fill="black", width=width)

    def draw_rect(self, coords, width):
        self.d.rectangle(coords, outline="black", width=width)

    def paste_im(self, path):
        to_paste = Image.open(path)
        self.image.paste(to_paste, box=(0, self.current_h))
        self.current_h += to_paste.height

    def center_paste(self, im, width, border=0):
        scale_factor = im.width / width
        new_height = im.height / scale_factor
        im = im.resize((width, round(new_height)))

        im = ImageOps.expand(im, border)

        x = (384 - im.width) // 2
        self.image.paste(im, box=(x, self.current_h))
        self.current_h += im.height

    def add_whitespace(self, space):
        self.current_h += space

    def draw_center_text(self, text, font, size, add_offset=0, spacing=4):
        font = ImageFont.truetype(font, size)
        self.boxcoords = self.d.textbbox((self.width / 2, self.current_h), text, anchor="ma", font=font, align="center",
                                         spacing=spacing)
        offset = self.boxcoords[1] - self.current_h
        self.d.text((self.width / 2 + add_offset, self.current_h - offset), text, fill="black", font=font,
                    align="center", spacing=spacing, anchor="ma")
        # self.boxcoords = self.d.textbbox((self.width/2 + add_offset, self.current_h - offset), text, anchor="ma", font=font, align="center", spacing=4)
        # self.d.rectangle(self.boxcoords, outline="black")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def draw_width(self, text, font, width, offset=0, alignment="c"):
        size = 1
        self.boxcoords = self.d.textbbox((0, 0), text, ImageFont.truetype(font, size))
        while self.boxcoords[2] - self.boxcoords[0] <= width:
            size += 1
            self.boxcoords = self.d.textbbox((0, 0), text, ImageFont.truetype(font, size))

        if alignment == "c":
            self.draw_center_text(text, font, size, add_offset=offset)
        elif alignment == "r":
            self.draw_right_text(text, font, size, add_offset=offset)
        elif alignment == "l":
            self.draw_left_text(text, font, size, add_offset=offset)

    def draw_left_text(self, text, font, size, add_offset=0, spacing=4):
        font = ImageFont.truetype(font, size)
        self.boxcoords = self.d.textbbox((self.width / 2, self.current_h), text, anchor="la", font=font, align="left",
                                         spacing=4)
        offset = self.boxcoords[1] - self.current_h
        self.d.text((add_offset, self.current_h - offset), text, fill="black", font=font, align="left", spacing=spacing,
                    anchor="la")
        # self.boxcoords = self.d.textbbox((add_offset, self.current_h - offset), text, font=font, align="left", spacing=spacing, anchor="la")
        # self.d.rectangle(self.boxcoords, outline="black")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def draw_right_text(self, text, font, size, add_offset=0, spacing=4):
        font = ImageFont.truetype(font, size)
        self.boxcoords = self.d.textbbox((self.width / 2, self.current_h), text, anchor="ra", font=font, align="right",
                                         spacing=spacing)
        offset = self.boxcoords[1] - self.current_h
        self.d.text((self.width - add_offset, self.current_h - offset), text, fill="black", font=font, align="right",
                    spacing=spacing, anchor="ra")
        # self.boxcoords = self.d.textbbox((self.width - add_offset, self.current_h - offset), text, anchor="ra", font=font, align="right", spacing=4)
        # self.d.rectangle(self.boxcoords, outline="black")
        h_increment = self.boxcoords[3] - self.boxcoords[1]
        self.current_h += h_increment

    def text_wrap(self, text, font, size, max_width, alignment="c", offset=0, spacing=4):

        font_t = ImageFont.truetype(font, size)
        wordlist = text.split(" ")
        line = []
        textlist = []

        for word in wordlist:

            line.append(word)
            linewidth = self.d.textbbox((0, 0), " ".join(line), font=font_t)[2]

            if linewidth > max_width:
                textlist += [line[:-1]]
                line = [line[-1]]

        textlist += [line]

        if not textlist[0]:
            textlist.pop(0)

        text = "\n".join([" ".join(part) for part in textlist])

        if alignment == "c":
            self.draw_center_text(text, font, size, add_offset=offset, spacing=spacing)
        elif alignment == "r":
            self.draw_right_text(text, font, size, add_offset=offset, spacing=spacing)
        elif alignment == "l":
            self.draw_left_text(text, font, size, add_offset=offset, spacing=spacing)

    def draw_underline(self, offfset, w):
        x1, y1 = self.boxcoords[0], self.boxcoords[3] + offfset
        x2, y2 = self.boxcoords[2], self.boxcoords[3] + offfset
        self.d.line((x1, y1, x2, y2), "black", width=w)
        self.current_h += offfset + w

    def show(self):
        return self.image.crop((0, 0, self.width, self.current_h))


def stitch_images(imagelist):

    totalheight = sum([image.height for image in imagelist])
    height = 0

    image = Image.new("RGB", (384, totalheight), "white")

    for im in imagelist:
        image.paste(im, box=(0, height))
        height += im.height

    image.show()

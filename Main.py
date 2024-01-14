from PIL import Image, ImageDraw, ImageFont

width = 384

im = Image.new("RGB", (width, 500), "white")

# Function that draws aligned text on image (location, text, font,

wagner = "NT Wagner.otf"
franchise = "Franchise.ttf"
clab = "Clab.otf"
product = "Product Sans Regular.ttf"
blackout = "Blackout Sunrise.ttf"
dillan = "Dillan.otf"
deco = "Deco.ttf"

def draw_text(image, h, text, font, size,  alignment=None):
    d = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, size)
    d.text((width/2, h), text, fill="black", font=font, anchor="mt")

draw_text(im, 30, "Augustus", deco, 65)
ImageDraw.Draw(im).line((70, 100, 310, 100), fill="black", width=2)
draw_text(im, 120, "25", deco, 200)
draw_text(im, 300, "Donderdag", franchise, 55)

im.show()
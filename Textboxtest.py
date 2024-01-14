from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("Franchise.ttf", 48)
im = Image.new("RGB", (200, 200), "white")
d = ImageDraw.Draw(im)
d.line(((0, 100), (200, 100)), "gray")
d.line(((100, 0), (100, 200)), "gray")
d.text((100, 0), "Anchor", fill="Black", anchor="mt", font=font)
textbox = d.textbbox((100, 0), "Anchor", anchor="mt", font=font)
d.rectangle(textbox, width=2, outline="Black")

im.show()
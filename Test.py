from PIL import Image, ImageDraw, ImageFont

chalk = ImageFont.truetype("Franchise.ttf",80)
prod = ImageFont.truetype("Super Dream.ttf", 250)

def text_center(text, image, x, y, font):
    ImageDraw.Draw(image).text((x,y), text, fill="black", font=font)


canvas = Image.new('RGB', (384,500), 'white')
text_center("Januari", canvas, 50, 20, chalk)
text_center("26", canvas, 93, 50, prod)

canvas.show()


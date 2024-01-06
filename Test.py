from PIL import Image, ImageDraw, ImageFont

chalk = ImageFont.truetype("Franchise.ttf",80)
prod = ImageFont.truetype("Product Sans Regular", 350)

def text_center(text, image, x, y, font):
    ImageDraw.Draw(image).text((x,y), text, fill="black", font=font)

canvas = Image.new('RGB', (384,500), 'white')
text_center("Januari", canvas, 90, 20, chalk)
text_center("6", canvas, 93, 15, prod)

canvas.show()


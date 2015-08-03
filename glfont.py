from PIL import Image, ImageDraw, ImageFont
from numpy import *


def load_font(filename, size):
    return ImageFont.truetype(filename, size)


def render_text(font, text, color, size):
    sz = font.getsize(text)[0], size
    img = Image.new("RGBA", sz, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, color, font=font)
    return sz[0], sz[1], concatenate(img.getdata())

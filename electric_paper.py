#! /usr/bin/env python
import serial as ser
import io
from PIL import Image, ImageDraw, ImageFont
import argparse


def create_image(text):
    img = Image.new(
        "1", (
            25 * 8,
            96,
        ), color=1)

    if len(text) <= 2:
        size = 48
        pos = (45, 26)
    elif len(text) <= 3:
        size = 48
        pos = (30, 26)
    elif len(text) <= 6:
        size = 36
        pos = (5, 26)
    else:
        size = 30
        pos = (5, 34)

    unicode_font = ImageFont.truetype("./RictyDiminishedDiscord-Regular.ttf",
                                      size)
    draw = ImageDraw.Draw(img)
    draw.text(pos, text, font=unicode_font, fill=0)
    del draw

    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='BMP')
    barr = bytearray(imgByteArr.getvalue())
    barr[0x26] = 0x00
    barr[0x2A] = 0x00
    barr[0x2E] = 0x00
    barr[0x32] = 0x00
    return bytes(barr)


if __name__ == '__main__':
    # electric_paper.py COM3 "会議中"  for windows
    # electric_paper.py /dev/ttyUSB0 for linux
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('port', metavar='PORT', type=str, help='port')
    parser.add_argument(
        'message', metavar='MESSAGE', type=str, help='message to show')

    args = parser.parse_args()
    print("show message")
    ser = ser.Serial(args.port, 115200)
    ser.write(create_image(args.message))
    ser.close()
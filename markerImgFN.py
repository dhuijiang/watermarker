#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import re
import os
import sys

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops

# TTF_FONT = u'./font/青鸟华光简琥珀.ttf'
TTF_FONT = os.path.join("font", "msyh.ttc")
TTF_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), TTF_FONT)

def add_mark(imagePath, args):
    '''
    添加文件名水印，然后保存图片
    '''
    fileName = os.path.basename(imagePath)
    imageName = os.path.splitext(fileName)[0]

    result = re.search(args.pattern, imageName)
    if not result:
        print("%s: regex pattern \"%s\" matches \"%s\" Failed." % (fileName,  args.pattern, imageName))
        return

    text = result.group(1)

    print("%s: drawing \"%s\" in ..." % (fileName, text), end=" ")
    try:

        # 字体宽度
        width = len(text) * args.size

        im = Image.open(imagePath)

        x = im.size[0] - width * 0.65
        y = im.size[1] - args.size * 1.5
        
        # 生成文字
        draw_table = ImageDraw.Draw(im)
        draw_table.text(xy=(x, y),
                        text=text,
                        fill=args.color,
                        font=ImageFont.truetype(TTF_FONT,
                                                size=args.size))
        del draw_table

        # im.show()

        name = os.path.basename(imagePath)
        if not os.path.exists(args.out):
            os.mkdir(args.out)

        new_name = os.path.join(args.out, name)

        im.save(new_name)

    except:
        print("Failed.")
        return

    print("Completed.")


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", "--file", type=str,
                       help="image file path or directory")
    parse.add_argument("-p", "--pattern", default="^(.*)-\d$", type=str,
                       help="regex pattern, matches the image file names $1 group as the watermark content, default is '^(.*)-\d$'")
    parse.add_argument("-c", "--color", default="#FF0000", type=str,
                       help="text color like '#000000', default is #FF0000")
    parse.add_argument("-o", "--out", default="./output",
                       help="image output directory, default is ./output")
    parse.add_argument("--size", default=50, type=int,
                    help="font size of text, default is 50")

    args = parse.parse_args()

    if isinstance(args.pattern, str) and sys.version_info[0] < 3:
        args.pattern = args.pattern.decode("utf-8")

    if os.path.isdir(args.file):
        names = os.listdir(args.file)
        for name in names:
            image_file = os.path.join(args.file, name)
            add_mark(image_file, args)
    else:
        add_mark(args.file, args)


if __name__ == '__main__':
    main()

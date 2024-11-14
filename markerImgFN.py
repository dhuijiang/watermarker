#!/usr/bin/python
# -*- coding: utf-8 -*-
# example:
#    python .\markerImgFN.py -f .\input\KTG061-1.png -m "NAME: " "name:([^-]+)" -m "FROM: Water Marker" -m "DATE: " "csv:.\input\datekvs.csv"
# completed info: 
#    KTG061-1.png: drawing "['NAME: KTG061', 'FROM: Water Marker', 'DATE: 2024-11-14']" in ... Completed.

import argparse
import re
import os
import sys

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops

# TTF_FONT = u'./font/青鸟华光简琥珀.ttf'
TTF_FONT = os.path.join("font", "NotoSansMonoCJKsc-Regular.otf")
TTF_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), TTF_FONT)

def add_mark(imagePath, args):
    '''
    添加文件名水印，然后保存图片
    '''
    fileName = os.path.basename(imagePath)
    imageName = os.path.splitext(fileName)[0]

    texts = []
    for marks in args.mark:
        text = ""
        for mark in marks:
            if mark.startswith("name:"):
                result = re.search(mark[5:], imageName)
                if result:
                    groups = list(result.groups())
                    text += ''.join(groups)
            elif mark.startswith("csv:"):
                csvfile = mark[4:]
                with open(csvfile) as f:
                    import csv
                    reader = csv.reader(f)
                    for row in reader:
                        if row[0] == imageName:
                            text += row[1]
                            break
            else:
                text += mark
        texts.append(text)
    #print("Watermark contents: ", texts)
    
    max_length = max(len(text) for text in texts) if texts else 0
    #print("Watermark contents max length: ", max_length)
    
    text = '\n'.join(texts)

    print("%s: drawing \"%s\" in ..." % (fileName, texts), end=" ")
    try:

        # 字体宽度
        #width = len(text) * args.size
        width = max_length * args.size

        im = Image.open(imagePath)

        x = im.size[0] - width * 0.55
        y = im.size[1] - args.size * 1.5 * len(texts)
        
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

    except Exception as e:
        print(f"Failed. {e}")
        return

    print("Completed.")


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", "--file", type=str,
                       help="image file path or directory")
    parse.add_argument("-m", "--mark", type=str, nargs="*", action="append",
                       help="watermark content (e.g. -m \"<text>\" or -m \"name:<pattern>\" or -m \"csv:<csvfile>\"), <pattern> matches the image file names groups as the watermark content, <csvfile> matches key-value pairs in the csv file using image file name as key and value as the watermark content")
    parse.add_argument("-c", "--color", default="#FF0000", type=str,
                       help="text color like '#000000', default is #FF0000")
    parse.add_argument("--size", default=50, type=int,
                       help="font size of text, default is 50")
    parse.add_argument("-o", "--out", default="./output",
                       help="image output directory, default is ./output")

    args = parse.parse_args()

    if not args.file:
        print("Error: The -f/--file parameter is required.")
        sys.exit(1)

    #if isinstance(args.pattern, str) and sys.version_info[0] < 3:
    #    args.pattern = args.pattern.decode("utf-8")

    if os.path.isdir(args.file):
        names = os.listdir(args.file)
        for name in names:
            image_file = os.path.join(args.file, name)
            add_mark(image_file, args)
    else:
        add_mark(args.file, args)


if __name__ == '__main__':
    main()
